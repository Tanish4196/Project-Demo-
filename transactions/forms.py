from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import IssueBook
from books.models import Book
from accounts.models import Student


class BookIssueForm(forms.Form):
    """Form for issuing books to students"""
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available__gt=0),
        label="Name of Book",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        max_length=200,
        label="Author Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Auto-populated'
        })
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    issue_date = forms.DateField(
        label="Issue Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'readonly': True
        })
    )
    return_date = forms.DateField(
        label="Return Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        return_date = cleaned_data.get('return_date')
        book = cleaned_data.get('book')

        # Validate issue date is not less than today
        if issue_date and issue_date < datetime.now().date():
            raise ValidationError("Issue date cannot be less than today.")

        # Validate return date is 15 days from issue date
        if issue_date and return_date:
            max_return_date = issue_date + timedelta(days=15)
            if return_date > max_return_date:
                raise ValidationError(
                    f"Return date cannot be greater than 15 days from issue date ({max_return_date})."
                )
            if return_date < issue_date:
                raise ValidationError("Return date cannot be before issue date.")

        # Validate book availability
        if book and book.available <= 0:
            raise ValidationError("This book is not available.")

        return cleaned_data


class ReturnBookForm(forms.Form):
    """Form for returning books"""
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        label="Name of Book",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        max_length=200,
        label="Author Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Auto-populated'
        })
    )
    serial_no = forms.CharField(
        max_length=50,
        label="Serial No of Book",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter serial number'
        })
    )
    issue_date = forms.DateField(
        label="Issue Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'readonly': True
        })
    )
    return_date = forms.DateField(
        label="Return Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        return_date = cleaned_data.get('return_date')
        serial_no = cleaned_data.get('serial_no')

        if not serial_no:
            raise ValidationError("Serial number is mandatory.")

        if issue_date and return_date and return_date < issue_date:
            raise ValidationError("Return date cannot be before issue date.")

        return cleaned_data


class FinePaymentForm(forms.Form):
    """Form for paying fines"""
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Student",
        widget=forms.Select(attrs={'class': 'form-control'}),
        disabled=True
    )
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        label="Book",
        widget=forms.Select(attrs={'class': 'form-control'}),
        disabled=True
    )
    fine_amount = forms.DecimalField(
        label="Fine Amount",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        }),
        disabled=True
    )
    fine_paid = forms.DecimalField(
        label="Fine Paid",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount paid'
        })
    )
    remarks = forms.CharField(
        label="Remarks",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter remarks'
        }),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        fine_paid = cleaned_data.get('fine_paid')

        if not fine_paid or fine_paid <= 0:
            raise ValidationError("Fine paid must be a positive amount.")

        return cleaned_data


class AddMembershipForm(forms.Form):
    """Form for adding membership"""
    MEMBERSHIP_CHOICES = (
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
    )

    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    membership_number = forms.CharField(
        max_length=20,
        label="Membership Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter membership number'
        })
    )
    membership_duration = forms.ChoiceField(
        choices=MEMBERSHIP_CHOICES,
        label="Membership Duration",
        initial='6_months',
        widget=forms.RadioSelect()
    )

    def clean(self):
        cleaned_data = super().clean()
        membership_number = cleaned_data.get('membership_number')

        if not membership_number:
            raise ValidationError("Membership number is mandatory.")

        return cleaned_data


class UpdateBookForm(forms.Form):
    """Form for updating book information"""
    BOOK_TYPE_CHOICES = (
        ('book', 'Book'),
        ('movie', 'Movie'),
    )

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        label="Select Book/Movie",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    book_type = forms.ChoiceField(
        choices=BOOK_TYPE_CHOICES,
        label="Type",
        initial='book',
        widget=forms.RadioSelect()
    )
    title = forms.CharField(
        max_length=200,
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        max_length=200,
        label="Author",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    isbn = forms.CharField(
        max_length=20,
        label="ISBN",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        label="Quantity",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        isbn = cleaned_data.get('isbn')
        quantity = cleaned_data.get('quantity')

        if not all([title, author, isbn, quantity]):
            raise ValidationError("All fields are mandatory.")

        if quantity < 0:
            raise ValidationError("Quantity cannot be negative.")

        return cleaned_data


class SearchBooksForm(forms.Form):
    """Form for searching available books"""
    search_query = forms.CharField(
        max_length=200,
        label="Search Books",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or ISBN'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        search_query = cleaned_data.get('search_query')

        if not search_query:
            raise ValidationError("Please enter a search query.")

        return cleaned_data


class UserManagementForm(forms.Form):
    """Form for user management"""
    USER_CHOICES = (
        ('new', 'New User'),
        ('existing', 'Existing User'),
    )

    user_type = forms.ChoiceField(
        choices=USER_CHOICES,
        label="User Type",
        initial='new',
        widget=forms.RadioSelect()
    )
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        address = cleaned_data.get('address')

        if not all([username, email, phone, address]):
            raise ValidationError("All fields are mandatory.")

        return cleaned_data
