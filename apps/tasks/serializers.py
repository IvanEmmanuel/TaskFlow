from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):  #  significa que estamos creando un serializer basado en un modelo Django.
    
    class Meta:
        model = Task            #   Este serializer trabaja con nuestro modelo Task.
        fields = "__all__"      #  Incluye todos los campos del modelo.