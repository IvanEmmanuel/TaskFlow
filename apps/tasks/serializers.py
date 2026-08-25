from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):  #  significa que estamos creando un serializer basado en un modelo Django.
    
    class Meta:
        model = Task            #   Este serializer trabaja con nuestro modelo Task.
        fields = "__all__"      #  Incluye todos los campos del modelo.
        
        read_only_fields = [    # el cliente no podrá trabajar con estos campos, solo Django
            "id",
            "created_at",
            "updated_at",
            "user",
        ]
        
class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only = True                   #  El cliente puede enviar la contraseña, pero la API nunca debe devolverla.
    )
    
    password_confirmation = serializers.CharField(
        write_only=True                     #  El cliente puede enviar la contraseña, pero la API nunca debe devolverla.
    )
    
#     trabaja con
#        ↓
#       User
#        ↓
# solamente expondrá
#        ↓
# username, email, password
    
    class Meta:
        model = User
        fields = [
                "username", 
                "email", 
                "password", 
                "password_confirmation",
        ]
        
    def validate(self, attrs):                                  # attrs contiene los datos que DRF ya recibió y validó.
        if attrs["password"] != attrs["password_confirmation"]: # Si son diferentes:
            raise serializers.ValidationError(
                "Las contraseñas no coinciden."
            )
        return attrs
    
    def create(self, validated_data):                           # Aquí es donde vamos a convertir los datos validados en un objeto User.
        validated_data.pop("password_confirmation")             # la eliminamos porque no pertenece al modelo User, solo la usamos para confirmar
        
        user = User.objects.create_user(
            username= validated_data["username"],
            email= validated_data["email"],
            password= validated_data["password"],
        )
        
        return user