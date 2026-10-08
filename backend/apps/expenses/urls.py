from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expenses, name='expenses-list-create'),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense-detail'),
]
