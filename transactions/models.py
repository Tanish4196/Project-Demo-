# Create your models here.
from django.db import models
from books.models import Book
from accounts.models import Student
from datetime import timedelta
from django.utils import timezone

class IssueBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)

    returned = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.book}"
    
    def calculate_fine(self):
        """Calculate fine if book is returned late"""
        if not self.returned:
            today = timezone.now().date()
            if today > self.return_date:
                days_late = (today - self.return_date).days
                self.fine_amount = days_late * 10  # 10 rupees per day
        return self.fine_amount
    
    def mark_returned(self, actual_return_date=None):
        """Mark book as returned and update inventory"""
        self.returned = True
        self.actual_return_date = actual_return_date or timezone.now().date()
        self.calculate_fine()
        self.book.available += 1
        self.book.save()
        self.save()


class Fine(models.Model):
    """Model to track fine payments"""
    issue_book = models.OneToOneField(IssueBook, on_delete=models.CASCADE, related_name='fine')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fine for {self.issue_book}"
    
    def mark_paid(self, paid_amount):
        """Mark fine as paid"""
        self.paid_amount = paid_amount
        self.paid_date = timezone.now().date()
        self.is_paid = True
        self.save()