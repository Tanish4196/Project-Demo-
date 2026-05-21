# Register your models here.
from django.contrib import admin
from .models import IssueBook, Fine

@admin.register(IssueBook)
class IssueBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issue_date', 'return_date', 'returned', 'fine_amount')
    search_fields = ('student__user__username', 'book__title')
    list_filter = ('returned', 'issue_date')
    readonly_fields = ('issue_date',)

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('issue_book', 'fine_amount', 'paid_amount', 'is_paid', 'paid_date')
    search_fields = ('issue_book__student__user__username', 'issue_book__book__title')
    list_filter = ('is_paid', 'paid_date')
    readonly_fields = ('issue_book', 'fine_amount')