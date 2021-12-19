
from django import forms
from django.forms import widgets
from .models import Respuesta,Pregunta

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from .globals import *

class RespuestaForm(forms.Form):
    idRpta = forms.HiddenInput()
    like = forms.TextInput( )
    dislike = forms.TextInput( )

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = [
            'usuario',
            'categoria',
            'titulo',
            'descripcion',
            'confiable',
            'keywords',
        ]

        widgets = {
            'usuario':widgets.HiddenInput(),
            'confiable':widgets.HiddenInput(),
        }

class CreateReply(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields=[
            "usuario",
            "pregunta",
            "descripcion",
            "url_img",
            "likes",
            "dislikes"
        ]
        widgets  = {
            "usuario":widgets.TextInput(attrs={'readonly': 'readonly'}),
            "pregunta":widgets.TextInput(attrs={'readonly': 'readonly'}),
            "descripcion":widgets.Textarea(),
            "url_img":widgets.TextInput(),
            "likes":widgets.NumberInput(attrs={'readonly': 'readonly'}),
            "dislikes":widgets.NumberInput(attrs={'readonly': 'readonly'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required= True)

    class Meta:
        model = Usuario
        fields = (
                'username',
                'email',
                'password1',
                'password2'
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
