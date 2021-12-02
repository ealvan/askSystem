from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from .models import Categoria, Pregunta,Respuesta, Usuario
from django.db.models import Q

from .forms import CreateReply, PreguntaForm,RespuestaForm

# Create your views here.
def index(request):
    return render(request,'base.html',{})

def resultados(request):
    if request.method == "POST":
        busqueda = request.POST.get("buscar")
        confiable = request.POST.get("confiable")
        preguntas = {}
        if(confiable):
            preguntas = Pregunta.objects.filter(
                Q(descripcion__icontains = busqueda) |
                Q(titulo__icontains = busqueda) |
                Q(keywords__icontains = busqueda),
                confiable = True
                ).distinct()
        else:
            if busqueda:
                preguntas = Pregunta.objects.filter(
                    Q(descripcion__icontains = busqueda) |
                    Q(titulo__icontains = busqueda) |
                    Q(keywords__icontains = busqueda)
                    ).distinct()
            
        return render(request,'resultados.html',{'preguntas':preguntas})
    else:
        return render(request,'resultados.html',{})

def preguntaConfiable(request):
    confiables = Pregunta.objects.filter(confiable=True)
    context = {
        "confiables":confiables
    }
    return render(request,"main/preguntaConfiable.html",context)

def rawListQuestion(request):
    confiables = Pregunta.objects.all()
    context = {
        "lista":confiables
    }
    return render(request,"main/rawListQuestions.html",context)    


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

def createReply(request,question_id):
    # print("Question ID: ",question_id)
    if request.method == "GET":
        question = get_object_or_404(Pregunta, id=question_id)
        if question:
            context = {
                "question":question
            }
            return render(request,"main/createReply.html",context)            
        else:
            return render(request,"main/createReply.html")
    else:
        form = CreateReply(request.POST)

    return render(request,"main/createReply.html")


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



