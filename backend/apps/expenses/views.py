from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Expense, Category, BankAccount
from .serializers import ExpenseSerializer

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def expenses(request):
    """
    Gère la récupération de la liste des dépenses de l'utilisateur ou la création d'une nouvelle dépense.
    """
    if request.method == "GET":
        # Retourne uniquement les dépenses appartenant à l'utilisateur connecté
        user_expenses = Expense.objects.filter(user=request.user).order_by('-date')
        serializer = ExpenseSerializer(user_expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        amount = request.data.get("amount")
        description = request.data.get("description")
        bank_account_id = request.data.get("bank_account")
        category_id = request.data.get("category")
        date = request.data.get("date")

        # Validation backend : vérifier la présence des champs obligatoires
        if amount is None:
            return Response({"error": "Le montant est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
        if not description:
            return Response({"error": "La description est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
        if not bank_account_id:
            return Response({"error": "Le compte bancaire est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
        if not date:
            return Response({"error": "La date est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que le compte bancaire existe et appartient bien à l'utilisateur
        try:
            bank_account = BankAccount.objects.get(id=bank_account_id, user=request.user)
        except BankAccount.DoesNotExist:
            return Response({"error": "Le compte bancaire spécifié n'existe pas ou ne vous appartient pas."}, status=status.HTTP_403_FORBIDDEN)

        # Vérifier la catégorie si elle est fournie
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response({"error": "La catégorie spécifiée n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        # Création de la dépense
        expense = Expense.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            bank_account=bank_account,
            category=category,
            transaction_type=request.data.get("transaction_type", "expense"),
            date=date
        )

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def expense_detail(request, expense_id):
    """
    Gère la consultation, la modification ou la suppression d'une dépense spécifique.
    """
    # Récupérer la dépense en s'assurant qu'elle appartient à l'utilisateur connecté
    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
    except Expense.DoesNotExist:
        return Response({"error": "La dépense spécifiée n'existe pas ou ne vous appartient pas."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        amount = request.data.get("amount")
        description = request.data.get("description")
        bank_account_id = request.data.get("bank_account")
        category_id = request.data.get("category")
        date = request.data.get("date")
        transaction_type = request.data.get("transaction_type")

        # Mise à jour conditionnelle des champs
        if amount is not None:
            expense.amount = amount
        if description is not None:
            expense.description = description
        if date is not None:
            expense.date = date
        if transaction_type is not None:
            expense.transaction_type = transaction_type

        # Mise à jour du compte bancaire (en vérifiant les permissions)
        if bank_account_id is not None:
            try:
                bank_account = BankAccount.objects.get(id=bank_account_id, user=request.user)
                expense.bank_account = bank_account
            except BankAccount.DoesNotExist:
                return Response({"error": "Le compte bancaire spécifié n'existe pas ou ne vous appartient pas."}, status=status.HTTP_403_FORBIDDEN)

        # Mise à jour de la catégorie
        if category_id is not None:
            try:
                category = Category.objects.get(id=category_id)
                expense.category = category
            except Category.DoesNotExist:
                return Response({"error": "La catégorie spécifiée n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        expense.save()
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
