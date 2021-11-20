from django.shortcuts import render
from .models import Pregunta
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





