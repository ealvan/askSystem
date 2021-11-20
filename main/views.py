from django.shortcuts import render
from django.views.generic import ListView
from .models import Pregunta

# Create your views here.
def preguntaConfiable(request):
    confiables = Pregunta.objects.filter(confiable=True)
    context = {
        "confiables":confiables
    }
    return render(request,"main/preguntaConfiable.html",context)

class PreguntaListView(ListView):
    model = Pregunta