
from django import forms
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
