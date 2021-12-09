
from django import forms
from django.forms import widgets
from .models import Respuesta,Pregunta

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
