from django.urls import path
from . import views
from transactions import views as transaction_views

urlpatterns = [
    path('', transaction_views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', transaction_views.book_list, name='book_list'),
    path('issue-book/', transaction_views.issue_book, name='issue_book'),
    path('return-book/', transaction_views.return_book, name='return_book'),
    path('pay-fine/<int:fine_id>/', transaction_views.pay_fine, name='pay_fine'),
    path('add-membership/', transaction_views.add_membership, name='add_membership'),
    path('update-book/', transaction_views.update_book, name='update_book'),
    path('search-books/', transaction_views.search_books, name='search_books'),
    path('manage-users/', transaction_views.manage_users, name='manage_users'),
]