#  views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from transactions.views import home, book_list

# Home page
def dashboard(request):
    """Dashboard view - redirects to home"""
    return home(request)