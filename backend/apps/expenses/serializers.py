from rest_framework import serializers
from .models import Expense, BankAccount, Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Category.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

class BankAccountSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle BankAccount.
    """
    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'balance', 'user']
        read_only_fields = ['user']

class ExpenseSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Expense.
    """
    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'bank_account', 'amount', 'description', 
            'category', 'transaction_type', 'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
