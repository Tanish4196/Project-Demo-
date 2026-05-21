from django.urls import path
from . import views

urlpatterns = [

    path(
        'return/<int:issue_id>/',
        views.return_book,
        name='return_book'
    ),

]