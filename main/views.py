from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.urls import reverse_lazy
from .models import Categoria, Globales, Pregunta,Respuesta, Usuario
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
from random import randint

from .forms import SignUpForm
# Create your views here. Falta arreglar el mandar solo 3 preguntas

def get_random_item():
    count = Pregunta.objects.count()
    rand = randint(0,count-3)
    a = Pregunta.objects.filter(id__range=[rand, rand+2])

def index(request): #Se envian solo 3 objetos aleatorios
    preguntas = Pregunta.objects.all()
    count = Pregunta.objects.count()
    print(count)
    rand = randint(1,count-2)
    q = get_object_or_404(Pregunta, id=rand)
    a = Pregunta.objects.filter(id__range=[rand+1, rand+2])

    context = {
        "lista":a,
        "q":q,
    }
    return render(request,"base.html",context)

#Es posible prrarlo, no se usa
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

            print("asd")
            tryConfiable(post.usuario.id,question_id)
            trySubNivel(post.usuario.id)
            tryConfiablRpta(post)
            print("asd" + str(GetLikeGlobal()))


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
            trySubNivel(post.usuario.id)
            tryConfiablRpta(post)
            return HttpResponseRedirect(reverse('question', kwargs={"question_id": question_id }))

    context = {
        "question": question,
        "rptas":orderByLikes(questionID=question.id),
    }
    return render(request, "main/singleQuestion.html",context)

def rptasConfiables(request,question_id):
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

            print("asd")
            tryConfiable(post.usuario.id,question_id)
            trySubNivel(post.usuario.id)
            tryConfiablRpta(post)
            print("asd" + str(GetLikeGlobal()))


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
            trySubNivel(post.usuario.id)
            tryConfiablRpta(post)
            return HttpResponseRedirect(reverse('question', kwargs={"question_id": question_id }))

    context = {
        "question": question,
        "rptas":orderByLikes(questionID=question.id),
    }
    return render(request, "main/rptasConfiables.html",context)

def orderByLikes(questionID):
    rptas = Respuesta.objects.filter(pregunta=questionID)
    orderList = sorted(rptas,key=lambda x: x.like.count(), reverse=True)
    return orderList

def tryConfiablRpta(post):

    if(post.like.count() >= GetLikeGlobal()): #Necesaria variable global
        post.confiable = True
    else:
        post.confiable = False
    post.save()


def tryConfiable(id, question_id):
    a = Respuesta.objects.filter(pregunta=question_id)
    q = get_object_or_404(Pregunta, id=question_id)

    cont_aux_likes = 0;
    for asd in a: #Likes necesarios
        if(asd.like.count() >= GetLikeGlobal()):
            print("bruh! " + str(asd.like.count()))
            cont_aux_likes += 1
    print("LOS LIKES VISTOS  "  + str(cont_aux_likes))
    if cont_aux_likes > 1:
        q.confiable = True
    else:
        q.confiable = False
    q.save()

def trySubNivel(id):
    a = Respuesta.objects.filter(usuario=id)
    q = get_object_or_404(Usuario, id=id)
    cont_aux_likes = 0;
    for asd in a:
        if(asd.like.count() >= GetLikeGlobal()):
            cont_aux_likes += 1
    if cont_aux_likes == 1:
        q.nivel = 5
    else:
        if cont_aux_likes == 2:
            q.nivel = 4
        else:
            if cont_aux_likes == 3:
                q.nivel = 3
            else:
                if cont_aux_likes == 4:
                    q.nivel = 2
                else:
                    if cont_aux_likes >= 5:
                        q.nivel = 1
    q.save()



    print("hola")


def createReply(request, question_id):
    # print("Question ID: ",question_id)

    if request.method == "GET":
        question = get_object_or_404(Pregunta, id=question_id)
        if question:

            if request.user.is_authenticated:
                obj = Respuesta()
                obj.usuario = request.user
                obj.pregunta = question
                obj.descripcion = ""
                obj.likes = 0
                obj.dislikes = 0
                obj.url_img = ""
                form = create_reply(instance=obj)
                context = {
                    "question":question,
                    "usuario":request.user,
                    "form":form,
                }
                return render(request,"main/createReply.html",context)
            return render(request,"main/createReply.html")
        else:
            return render(request,"main/createReply.html")
    else:
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

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2 :
            if Usuario.objects.filter(username = username).exists():
                messages.info(request, 'Username existente')
                return redirect('/createuser')
            elif Usuario.objects.filter(email = email).exists():
                messages.info(request, 'Email Registrado')
                return redirect('/createuser')
            else:
                user = Usuario.objects.create_user(email = email,username = username, password = password1)
                user.save();

                print('user created')
                return redirect('/')
        else :
            messages.info(request, 'No coinciden las contraseñas')
            return redirect('/createuser')
        return redirect('/')
    else :
        return render(request, 'register.html')
#grafico pregunta

def PreguntaGraficoView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    respuestasDes = []
    likes = []
    dislikes = []
    for r in obj.get_respuestas():
        #respuestasDes.append(r.descripcion)
        #likes.append(r.likes)
        #dislikes.append(r.dislikes)

        #tomamos solo las respuestas confiables
        if r.confiable:
            respuestasDes.append(r.descripcion)
            likes.append(r.like.count())
            dislikes.append(r.dislike.count())
    context = {
        'titulo': obj.titulo,
        'respuestasDes': respuestasDes,
        'likes': likes,
        'dislikes': dislikes,
    }
    return render(request, 'main/pregunta_grafico.html', context)

def GetLikeGlobal():
    obLike = get_object_or_404(Globales, id = 1)
    return obLike.global_py_var

class ListCategories(ListView):
    model = Categoria
    template_name = "crudcat/listcat.html"

class AddCat(CreateView):
    model = Categoria
    fields = "__all__"
    template_name = "crudcat/addcat.html"
    success_url = reverse_lazy("listcat")

class EditCat(UpdateView):
    model = Categoria
    template_name = "crudcat/edit.html"
    fields = "__all__"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("listcat")

class DeleteCat(DeleteView):
    model = Categoria
    pk_url_kwarg = "pk"
    template_name = "crudcat/delcat.html"
    success_url = reverse_lazy("listcat")

def listUsers(request,pk):
    user = Usuario.objects.get(id=pk)
    context = {
        "usersended":user
    }
    return render(request,"usuario/list_usuario.html",context)

#HOla
def PreguntaGraficoView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    respuestasDes = []
    likes = []
    dislikes = []
    for r in obj.get_respuestas():
        #respuestasDes.append(r.descripcion)
        #likes.append(r.likes)
        #dislikes.append(r.dislikes)

        #tomamos solo las respuestas confiables
        if r.confiable:
            respuestasDes.append(r.descripcion)
            likes.append(r.like.count())
            dislikes.append(r.dislike.count())
    context = {
        'titulo': obj.titulo,
        'respuestasDes': respuestasDes,
        'likes': likes,
        'dislikes': dislikes,
    }
    return render(request, 'main/pregunta_grafico.html', context)

def RespuestaListConfiableView(request, question_id):
    obj = get_object_or_404(Pregunta, id = question_id)
    respuestasConfiables = []
    for r in obj.get_respuestas():
        if r.confiable:
            respuestasConfiables.append(r)
    context = {
        'object_list': respuestasConfiables,
        'id': obj.id,
    }
    return render(request, 'main/respuestas_confiables.html', context)