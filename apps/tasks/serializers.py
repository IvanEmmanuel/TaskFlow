from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Task

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer encargado de convertir objetos Task de Django
    en datos que puedan ser enviados mediante la API,
    normalmente en formato JSON.

    También permite validar y convertir los datos recibidos
    desde una petición de la API antes de crear o modificar
    objetos Task.
    """
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        # Indicamos que este serializer está relacionado
        # directamente con el modelo Task.
        model = Task

        # "__all__" incluye todos los campos definidos
        # en el modelo Task dentro del serializer.
        fields = "__all__"

        # Estos campos son administrados por Django y no
        # deben ser modificados directamente por el cliente, son solo de lectura.
        #
        # id:
        # Django lo genera automáticamente.
        #
        # created_at:
        # Django establece la fecha de creación mediante
        # auto_now_add=True.
        #
        # updated_at:
        # Django actualiza automáticamente este campo
        # mediante auto_now=True.
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
        ]
        
class RegisterSeralizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        
