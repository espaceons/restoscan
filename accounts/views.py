from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


# 1. Vue pour l'Inscription (Register)
class RegisterView(APIView):

  def post(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response(
          {
              'message': 'Utilisateur créé avec succès !',
              'user': {
                  'id': user.id,
                  'username': user.username,
                  'email': user.email,
                  'role': user.role,
              },
          },
          status=status.HTTP_201_CREATED,
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Vue pour la Connexion (Login avec JWT + renvoi du rôle)
class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer