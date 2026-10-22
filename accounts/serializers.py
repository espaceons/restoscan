from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# Serializer pour l'inscription
class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'role', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    password = validated_data.pop('password', None)
    user = super().create(validated_data)
    if password:
      user.set_password(password)
      user.save()
    return user


# Serializer personnalisé pour le Login (ajoute le rôle dans la réponse)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    # Ajouter des informations personnalisées dans le token si besoin
    token['username'] = user.username
    token['role'] = user.role
    return token

  def validate(self, attrs):
    data = super().validate(attrs)
    # Ajouter les infos de l'utilisateur dans la réponse JSON du login
    data['user'] = {
        'id': self.user.id,
        'username': self.user.username,
        'email': self.user.email,
        'role': self.user.role,
    }
    return data