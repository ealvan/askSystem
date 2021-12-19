from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from .models import Categoria, Pregunta,Respuesta, Usuario
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CreateReply as create_reply, PreguntaForm,RespuestaForm
import re
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout as do_logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .globals import *

from .forms import SignUpForm
# Create your views here.
def index(request):
    preguntas = Pregunta.objects.all()
    context = {
        "lista":preguntas
    }
    return render(request,"base.html",context)

def preguntas(request):
    preguntas = Pregunta.objects.all()
    context = {
        "lista":preguntas
    }
    return render(request,"resultados.html",context)


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

    if request.method == 'POST':
        tipo = request.POST.get("type")

        if tipo == "like":
            post = Respuesta.objects.get(pk= request.POST.get("rptaId"))
            print(post)
            is_dislike = False

            for dislike in post.dislike.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if is_dislike:
                post.dislike.remove(request.user)

            is_like = False

            for like in post.like.all():
                if like == request.user:
                    is_like = True
                    break

            if not is_like:
                post.like.add(request.user)

            if is_like: 
                post.like.remove(request.user)
            
            tryConfiable(post.usuario.id,question_id)


            return HttpResponseRedirect(reverse('question', kwargs={"question_id": question_id }))

        if tipo == "dislike":
            post = Respuesta.objects.get(pk=request.POST.get("rptaId"))
            is_like = False

            for like in post.like.all():
                if like == request.user:
                    is_like = True
                    break

            if is_like:
                post.like.remove(request.user)

            is_dislike = False

            for dislike in post.dislike.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if not is_dislike:
                post.dislike.add(request.user)

            if is_dislike:
                post.dislike.remove(request.user)

            tryConfiable(post.usuario.id,question_id)


            return HttpResponseRedirect(reverse('question', kwargs={"question_id": question_id }))

    context = {
        "question": question,
    }
    return render(request, "main/singleQuestion.html",context)

def tryConfiable(id, question_id):
    a = Respuesta.objects.filter(usuario=id)
    q = get_object_or_404(Pregunta, id=question_id)

    cont_aux_likes = 0;
    for asd in a:
        if(asd.like.count() >= 1):
            cont_aux_likes += 1
    if cont_aux_likes > 1:
        q.confiable = True
    else:
        q.confiable = False
    q.save()


    print("hola")

def createReply(request,username, question_id):
    # print("Question ID: ",question_id)

    if request.method == "GET":
        question = get_object_or_404(Pregunta, id=question_id)
        user = get_object_or_404(Usuario, id = username)
        if question:
            obj = Respuesta()
            obj.usuario = user
            obj.pregunta = question
            obj.descripcion = ""
            obj.likes = 0
            obj.dislikes = 0
            obj.url_img = ""
            form = create_reply(instance=obj)
            context = {
                "question":question,
                "usuario":user,
                "form":form,
            }

            return render(request,"main/createReply.html",context)
        else:
            return render(request,"main/createReply.html")
    else:
        user = get_object_or_404(Usuario, id = username)
        question = get_object_or_404(Pregunta, id=question_id)

        form = create_reply(request.POST)
        # pp.pprint(form.cleaned_data.get("descripcion"))
        if form.is_valid():
            #aqui no entra y no se porque, aqui lo dejo por hoy :(
            # print("AGHHHHHHHHHHHHHHHHHHHHHHHH")
            myCleanReply = Respuesta()
            try:
                myCleanReply.usuario = form.cleaned_data["usuario"]
                myCleanReply.pregunta = form.cleaned_data["pregunta"]
                myCleanReply.descripcion = form.cleaned_data["descripcion"]
                myCleanReply.likes = form.cleaned_data["likes"]
                myCleanReply.dislikes = form.cleaned_data["dislikes"]
                myCleanReply.url_img = form.cleaned_data["url_img"]
                myCleanReply.save()
            except:
                print("********NO SE PUDO GUARDAR BIEN!!!")
                return render(request,"main/rawListQuestions.html")

            # myCleanReply.save()
            #return render(request,"main/rawListQuestions.html")
            # # form.save()
            # pp.pprint(form.cleaned_data)
            #reverse() returns a string. form_valid() is supposed to return HTTP responses, not strings.
            return HttpResponseRedirect(reverse('question', kwargs={"question_id": question_id }))

        else:
            print("EL FORMULARIO NO ES VALIDO")

    return render(request,"main/createReply.html")

'''
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
'''

def listQuestion(request):
    preguntas = Pregunta.objects.all()
    context = {
        "lista":preguntas
    }
    return render(request,"listQuestions.html",context)    

class PreguntaListView(ListView):
    model = Pregunta

def PreguntaCreateView(request):

    form = PreguntaForm(request.POST or None, initial = {'usuario': request.user})
    if form.is_valid():
        form.save()
        form = PreguntaForm()
        return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'main/pregunta_form.html', context)
'''
if request.method == "POST":
        busqueda = request.POST.get("categoria")
        confiable = request.POST.get("titulo")
        confiable = request.POST.get("descripcion")
        confiable = request.POST.get("keywords")

'''
def PreguntaDetailView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    context = {
        'object': obj
    }
    return render(request, 'main/pregunta_detail.html', context)

class PreguntaDeleteView(DeleteView):
    model = Pregunta
    success_url = reverse_lazy('list')

class PreguntaUpdateView(UpdateView):
    model = Pregunta
    fields = {
        'categoria',
        'titulo',
        'descripcion',
        'keywords',   
    }

'''
def PreguntaDeleteView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    obj.delete()
    return HttpResponseRedirect(reverse('question'))

class PreguntaUpdateView(UpdateView):
    model = Pregunta
    fields = {
        'usuario',
        'categoria',
        'titulo',
        'descripcion',
        'confiable',
       





'''
def getUrlsandParse(descrp):
    re.findall(r"{*}")
    # return descrip
    pass

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			messages.info(request, 'Datos incorrectos')
			return HttpResponseRedirect(reverse('login'))
	else:
		return render(request, 'login.html')

def logout(request):
	#auth.logout(request)
	do_logout(request)
	return HttpResponseRedirect(reverse('index'))
def SignUp(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

#grafico pregunta

def PreguntaDetailView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    context = {
        'object': obj
    }
    return render(request, 'main/pregunta_detail.html', context)

def PreguntaGraficoView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    respuestasDes = []
    likes = []
    dislikes = []
    for r in obj.get_respuestas():
        respuestasDes.append(r.descripcion)
        likes.append(r.likes)
        dislikes.append(r.dislikes)
    context = {
        'titulo': obj.titulo,
        'respuestasDes': respuestasDes,
        'likes': likes,
        'dislikes': dislikes,
    }
    return render(request, 'main/pregunta_grafico.html', context)