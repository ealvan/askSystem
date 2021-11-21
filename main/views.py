from django.shortcuts import get_object_or_404, redirect, render
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

def singleQuestion(request,question_id):
    question = Pregunta.objects.get(id=question_id)
    context = {"question": question}
    return render(request, "main/singleQuestion.html",context)

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

def PreguntaDetailView(request, pk):
    obj = get_object_or_404(Pregunta, id = pk)

    context = {
        'object': obj
    }

    return render(request, 'main/pregunta_detail.html', context)