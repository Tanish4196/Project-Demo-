from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

from books.models import Book, Category
from accounts.models import Student
from transactions.models import IssueBook, Fine
from transactions.forms import (
    BookIssueForm, ReturnBookForm, FinePaymentForm,
    AddMembershipForm, UpdateBookForm, SearchBooksForm,
    UserManagementForm
)


def home(request):
    """Home/Dashboard view"""
    context = {
        'total_books': Book.objects.count(),
        'total_students': Student.objects.count(),
        'total_issued': IssueBook.objects.filter(returned=False).count(),
        'pending_returns': IssueBook.objects.filter(
            returned=False,
            return_date__lt=timezone.now().date()
        ).count(),
    }
    return render(request, 'dashboard.html', context)


def book_list(request):
    """Display all available books with search and filter"""
    books = Book.objects.filter(available__gt=0)
    categories = Category.objects.all()
    selected_category = None
    search_query = None

    # Handle category filter
    if request.GET.get('category'):
        category_id = request.GET.get('category')
        selected_category = get_object_or_404(Category, id=category_id)
        books = books.filter(category=selected_category)

    # Handle search
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )

    context = {
        'books': books,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'books/book_list.html', context)


@login_required
def issue_book(request):
    """Issue a book to a student"""
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            try:
                book = form.cleaned_data['book']
                student = form.cleaned_data['student']
                issue_date = form.cleaned_data['issue_date']
                return_date = form.cleaned_data['return_date']

                # Check if student has valid membership
                if not student.is_membership_valid():
                    messages.error(request, "Student membership is not valid. Please renew membership first.")
                    return redirect('issue_book')

                # Check book availability
                if book.available <= 0:
                    messages.error(request, "Book is not available.")
                    return redirect('issue_book')

                # Create issue record
                issue = IssueBook.objects.create(
                    student=student,
                    book=book,
                    issue_date=issue_date,
                    return_date=return_date
                )

                # Update book availability
                book.available -= 1
                book.save()

                messages.success(
                    request,
                    f"Book '{book.title}' issued successfully to {student.user.username}"
                )
                return redirect('book_list')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        # Set default dates
        initial_data = {
            'issue_date': timezone.now().date(),
            'return_date': timezone.now().date() + timedelta(days=15),
            'author': '',
        }
        form = BookIssueForm(initial=initial_data)

    context = {'form': form, 'page_title': 'Issue Book'}
    return render(request, 'transactions/issue_book.html', context)


@login_required
def return_book(request):
    """Return a book from a student"""
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            try:
                book = form.cleaned_data['book']
                serial_no = form.cleaned_data['serial_no']
                return_date = form.cleaned_data['return_date']

                # Get the issue record
                issue = IssueBook.objects.filter(
                    book=book,
                    returned=False
                ).first()

                if not issue:
                    messages.error(request, "No active issue record found for this book.")
                    return redirect('return_book')

                # Calculate fine if late
                if return_date > issue.return_date:
                    days_late = (return_date - issue.return_date).days
                    fine_amount = days_late * 10  # 10 rupees per day

                    # Create fine record
                    fine = Fine.objects.create(
                        issue_book=issue,
                        fine_amount=fine_amount
                    )

                    messages.warning(
                        request,
                        f"Book returned late. Fine amount: Rs. {fine_amount}. "
                        f"Please pay the fine to complete the transaction."
                    )
                    return redirect('pay_fine', fine_id=fine.id)

                # Mark as returned
                issue.mark_returned(return_date)
                messages.success(request, f"Book '{book.title}' returned successfully.")
                return redirect('book_list')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = ReturnBookForm(initial={'author': ''})

    context = {'form': form, 'page_title': 'Return Book'}
    return render(request, 'transactions/return_book.html', context)


@login_required
def pay_fine(request, fine_id):
    """Pay fine for late book return"""
    fine = get_object_or_404(Fine, id=fine_id)

    if request.method == 'POST':
        form = FinePaymentForm(request.POST)
        if form.is_valid():
            try:
                fine_paid = form.cleaned_data['fine_paid']
                remarks = form.cleaned_data['remarks']

                if fine_paid < fine.fine_amount:
                    messages.error(
                        request,
                        f"Paid amount (Rs. {fine_paid}) is less than fine amount (Rs. {fine.fine_amount})."
                    )
                    return redirect('pay_fine', fine_id=fine_id)

                # Mark fine as paid
                fine.mark_paid(fine_paid)
                fine.remarks = remarks
                fine.save()

                # Mark the issue as returned
                fine.issue_book.returned = True
                fine.issue_book.save()

                messages.success(request, f"Fine paid successfully. Change: Rs. {fine_paid - fine.fine_amount}")
                return redirect('book_list')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        initial_data = {
            'student': fine.issue_book.student,
            'book': fine.issue_book.book,
            'fine_amount': fine.fine_amount,
        }
        form = FinePaymentForm(initial=initial_data)

    context = {
        'form': form,
        'fine': fine,
        'page_title': 'Pay Fine'
    }
    return render(request, 'transactions/pay_fine.html', context)


@login_required
def add_membership(request):
    """Add or extend student membership"""
    if request.method == 'POST':
        form = AddMembershipForm(request.POST)
        if form.is_valid():
            try:
                student = form.cleaned_data['student']
                membership_number = form.cleaned_data['membership_number']
                duration = form.cleaned_data['membership_duration']

                # Map duration to days
                duration_map = {
                    '6_months': 180,
                    '1_year': 365,
                    '2_years': 730,
                }
                duration_days = duration_map.get(duration, 180)

                # Update student membership
                student.membership_number = membership_number
                student.extend_membership(duration_days)

                messages.success(
                    request,
                    f"Membership added for {student.user.username} "
                    f"(Valid until: {student.membership_end_date})"
                )
                return redirect('home')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = AddMembershipForm()

    context = {'form': form, 'page_title': 'Add Membership'}
    return render(request, 'transactions/add_membership.html', context)


@login_required
def update_book(request):
    """Update book information"""
    if request.method == 'POST':
        form = UpdateBookForm(request.POST)
        if form.is_valid():
            try:
                book = form.cleaned_data['book']
                title = form.cleaned_data['title']
                author = form.cleaned_data['author']
                isbn = form.cleaned_data['isbn']
                quantity = form.cleaned_data['quantity']

                # Update book
                book.title = title
                book.author = author
                book.isbn = isbn
                book.quantity = quantity
                book.save()

                messages.success(request, f"Book '{title}' updated successfully.")
                return redirect('book_list')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = UpdateBookForm()

    context = {'form': form, 'page_title': 'Update Book'}
    return render(request, 'transactions/update_book.html', context)


def search_books(request):
    """Search for available books"""
    books = []
    search_query = None

    if request.method == 'POST':
        form = SearchBooksForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            books = Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query),
                available__gt=0
            )
    else:
        form = SearchBooksForm()

    context = {
        'form': form,
        'books': books,
        'search_query': search_query,
        'page_title': 'Search Books'
    }
    return render(request, 'transactions/search_books.html', context)


@login_required
def manage_users(request):
    """Manage users (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')

    if request.method == 'POST':
        form = UserManagementForm(request.POST)
        if form.is_valid():
            try:
                user_type = form.cleaned_data['user_type']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']

                if user_type == 'new':
                    # Create new user
                    from django.contrib.auth.models import User
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='defaultpass123'
                    )
                    Student.objects.create(
                        user=user,
                        phone=phone,
                        address=address
                    )
                    messages.success(request, f"User '{username}' created successfully.")
                else:
                    # Update existing user
                    user = get_object_or_404(User, username=username)
                    user.email = email
                    user.save()

                    student = get_object_or_404(Student, user=user)
                    student.phone = phone
                    student.address = address
                    student.save()
                    messages.success(request, f"User '{username}' updated successfully.")

                return redirect('home')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = UserManagementForm()

    context = {'form': form, 'page_title': 'Manage Users'}
    return render(request, 'transactions/manage_users.html', context)