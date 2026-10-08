from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Modèle représentant une catégorie de dépense ou de revenu.
    Permet de classifier les transactions (ex: Alimentation, Loyer, etc.).
    """
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        """
        Retourne le nom de la catégorie sous forme de chaîne de caractères.
        """
        return str(self.name)

class BankAccount(models.Model):
    """
    Modèle représentant un compte bancaire appartenant à un utilisateur.
    Chaque dépense ou revenu sera associé à un compte bancaire.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    def __str__(self) -> str:
        """
        Retourne le nom du compte et l'utilisateur associé.
        """
        return f"{self.name} - {self.user.username}"

class Expense(models.Model):
    """
    Modèle représentant une transaction financière (revenu ou dépense).
    """
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Retourne une représentation textuelle de la dépense.
        """
        return f"{self.date} - {self.description} ({self.amount})"
