from django.db import models


# Create your models here.
class Usuario(models.Model):
    usuario = models.CharField(max_length=40,null=False,blank=False)
    password = models.CharField(max_length=80,null=False,blank=False)
    #solo habra 5 niveles, el mejor es el nivel 1, el default es 5
    nivel = models.IntegerField(default=5)
    correo = models.EmailField(max_length=100,null=False,blank=False)


class Categoria(models.Model):
    nombre = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(null=True,blank=True)

class Pregunta(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT)

    titulo = models.CharField(max_length=200,null=False,blank=False)
    descripcion = models.TextField(null=False,blank=False)
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


