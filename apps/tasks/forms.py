from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
# UserCreationForm es un formulario de Django diseñado
# específicamente para crear usuarios y validar sus contraseñas.
from django.contrib.auth.forms import UserCreationForm

# User es el modelo de usuario que proporciona Django.
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    
    
    
    # Django nos permite validar un campo específico mediante un método con esta estructura: 
    # def clean_nombre_del_campo(self):
    def clean_due_date(self):    # En TaskFlow, una fecha de vencimiento no puede estar en el pasado
        due_date = self.cleaned_data["due_date"] #nos proporciona el valor convertido a un objeto date, no simplemente el texto que llegó desde HTML.
        
        if due_date < timezone.localdate():
            
            #le dice a Django: Este campo contiene un dato que no cumple nuestras reglas.
            raise ValidationError( 
                # Entonces:  form.is_valid() -> en la vista
                # #devuelve: False
                # y no se ejecuta: form.save() -> en la vista
                # El formulario vuelve al template mostrando el error.
                "La fecha límite no puede ser anterior a hoy."
            )
            
        return due_date
    
    
    
    # Una tarea de prioridad HIGH no puede tener una fecha límite demasiado lejana.
    def clean(self):   #  Aquí estamos sobrescribiendo el método clean() que Django ya tiene en Form/ModelForm.
        #  "Django, haz primero tu validación normal y después déjame agregar mis propias reglas."
        cleaned_data = super().clean() #   super() significa:   Accede al comportamiento de la clase padre.
        
        due_date = cleaned_data.get("due_date") #  Después de la limpieza/conversión:  contiene los valores que Django considera válidos para continuar.
        priority = cleaned_data.get("priority")  #  De los datos ya limpiados por Django, dame el valor priority.
        
        if due_date and priority == "HIGH":
            max_date = timezone.localdate() + timedelta(days=30)
            
            if due_date > max_date:
                self.add_error(   # Este error proviene de una validación general, pero quiero asociarlo específicamente con el campo due_date.
                    "due_date",
                    "Una tarea de prioridad alta debe tener "
                    "una fecha límite dentro de los próximos 30 días."
                )
        
        return cleaned_data
    
    
    
    
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "status",
            "priority",
        ]
        
        labels = {
            "title": "Título",
            "description": "Descripción",
            "due_date": "Fecha límite",
            "status": "Estado",
            "priority": "Prioridad",
        }
        
        help_texts = {
            "title": "Escribe un título claro para la tarea.",
            "due_date": "Indica cuándo debe completarse la tarea.",
            "priority": "Selecciona qué tan importante es la tarea.",
        }
        
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Título de la tarea",
                }
            ),
            
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Descripción de la tarea",
                    "rows": 3,
                }
            ),
            
            "due_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }
        
# Nuestro formulario personalizado para registrar usuarios.
# Hereda de UserCreationForm para reutilizar sus validaciones
# y agregar el campo email.
class RegisterForm(UserCreationForm):

    class Meta:

        # Indicamos que el formulario trabajará con el modelo User.
        model = User

        # Campos que aparecerán en el formulario de registro.
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]