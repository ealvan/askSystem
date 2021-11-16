from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser

#por el momento no agregue imagFile o algo asi
#por que preseinto que el html, puede hacerlo con
#el tag <img>, asi nos ahorramos , seria para el frontend eso

# Create your models here.
class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    #password = models.CharField(max_length=80,null=False,blank=False)
    #solo habra 5 niveles, el mejor es el nivel 1, el default es 5
    nivel = models.IntegerField(default=5,null=True,blank=True)
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(null=True,blank=True)

class Pregunta(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT)

    titulo = models.CharField(max_length=200,null=False,blank=False)
    descripcion = models.TextField(null=False,blank=False)
#con rudy acordamos que es mejor un bool, para hacer un filtro de confiable
#nuestro plan es hacer una funcion que cambie este bool si hay una pregunta confiable
#las respuestas que tiene	
    confiable = models.BooleanField(default=False)
    #sera un JSON, que lo convertiremos a text con json.dumps(jsonobj)
    #y cuando lo recobremos sera con json.dump()
    #djnago no permite listas por el momento
    keywords = models.TextField(null=False,blank=False)


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta,on_delete=models.CASCADE)
    #queria agregarle titulo, pero creo esta demas
    #titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(null=False,blank=False)
    #se crea con 0 y 0 al inicio
    likes = models.IntegerField(default= 0)
    dislikes = models.IntegerField(default=0)


