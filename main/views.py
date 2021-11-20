from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import Pregunta

from .forms import PreguntaForm

# Create your views here.
def preguntaConfiable(request):
    confiables = Pregunta.objects.filter(confiable=True)
    context = {
        "confiables":confiables
    }
    return render(request,"main/preguntaConfiable.html",context)

class PreguntaListView(ListView):
    model = Pregunta

def PreguntaCreateView(request):
    form = PreguntaForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PreguntaForm()
        return redirect('main:pregunta-list')

    context = {
        'form': form
    }

    return render(request, 'main/pregunta_form.html', context)