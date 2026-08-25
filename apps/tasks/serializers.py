from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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
        validate_password(attrs["password"])                    # validación de contraseña ya utiliza los validadores configurados por Django.
        return attrs
    
    def validate_email(self, value):                            # DRF tiene validaciones específicas por campo.
        if User.objects.filter(email__iexact=value).exists():   # Para que la comparación sea insensible a mayúsculas/minúsculas.
            raise serializers.ValidationError(
                "Este email ya esta registrado."
            )
            
        return value
    
    def create(self, validated_data):                           # Aquí es donde vamos a convertir los datos validados en un objeto User.
        validated_data.pop("password_confirmation")             # la eliminamos porque no pertenece al modelo User, solo la usamos para confirmar
        
        user = User.objects.create_user(
            username= validated_data["username"],
            email= validated_data["email"],
            password= validated_data["password"],
        )
        
        return user
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="Refresh token que será invalidado."
    )