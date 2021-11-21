from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from .models import Pregunta,Respuesta

from .forms import PreguntaForm,RespuestaForm

# Create your views here.
def preguntaConfiable(request):
    confiables = Pregunta.objects.filter(confiable=True)
    context = {
        "confiables":confiables
    }
    return render(request,"main/preguntaConfiable.html",context)

def singleQuestion(request,question_id):
    
    data = request.GET
    if data:
        print(data)
        try:
            rptaId = int(data.get("rptaId"))
            typo = data.get("type")
            rptaObj = Respuesta.objects.get(id=rptaId)
        except:
            raise ValueError("Error al tratar con el **request.GET**")
        
        if typo == "like":
            rptaObj.likes += 1
        elif typo == "dislike":
            rptaObj.dislikes +=1
        else:
            print("ERROR de typo :", typo)
        rptaObj.save()
    question = Pregunta.objects.get(id=question_id)
    context = {
        "question": question,
    }
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