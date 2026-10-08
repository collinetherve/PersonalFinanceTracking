from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Connecte un utilisateur avec son nom d'utilisateur et son mot de passe.
    Retourne les informations de l'utilisateur en cas de succès.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Le nom d'utilisateur et le mot de passe sont obligatoires."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Vérifie les identifiants avec les mécanismes de hachage de Django
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Création de la session pour l'utilisateur
        login(request, user)
        return Response(
            {
                "message": "Connexion réussie.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Identifiants invalides."},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Déconnecte l'utilisateur courant en détruisant sa session.
    """
    logout(request)
    return Response(
        {"message": "Déconnexion réussie."},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Permet de créer un nouvel utilisateur.
    Les mots de passe sont hachés via user.set_password().
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response(
            {"error": "Le nom d'utilisateur et le mot de passe sont obligatoires."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Ce nom d'utilisateur est déjà pris."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Création de l'utilisateur avec mot de passe haché
    user = User(username=username, email=email)
    user.set_password(password)  # Hachage sécurisé du mot de passe
    user.save()

    return Response(
        {
            "message": "Utilisateur créé avec succès.",
            "user": {
                "id": user.id,
                "username": user.username,
            }
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Retourne les informations de l'utilisateur actuellement connecté.
    """
    user = request.user
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        status=status.HTTP_200_OK
    )
