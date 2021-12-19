from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,UserManager
from django.db.models.expressions import Value
from django.urls import reverse

class UsuarioManager(UserManager):
    def create_user(self, username, password=None,email=None, is_staff=False,is_admin=False,is_active=False):
        if not username:
            raise ValueError("username es obligatorio")
        if not password:
            raise ValueError("Obligatorio el password")
        user_obj = self.model(username = username)
        user_obj.set_password(password)
        user_obj.email = email
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    def create_staffuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
        )
        return user
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


#por el momento no agregue imagFile o algo asi
#por que presiento que el html, puede hacerlo con
#el tag <img>, asi nos ahorramos , seria para el frontend eso

# Create your models here.
class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, null=True)
    #password = models.CharField(max_length=80,null=False,blank=False)
    #solo habra 5 niveles, el mejor es el nivel 1, el default es 5
    nivel = models.IntegerField(default=5,null=True,blank=True)
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    active = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    objects = UsuarioManager()
    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin


class Categoria(models.Model):
    nombre = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse("listcat",args=[self.id,])
    def __str__(self):
        return self.nombre


class Pregunta(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria,null=True,on_delete=models.SET_NULL,blank=True)

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

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    def get_respuestas(self):
        return Respuesta.objects.filter(pregunta = self.id)


class Respuesta(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT,null=True,blank=True)
    pregunta = models.ForeignKey(Pregunta,on_delete=models.CASCADE)
    #imgs = models.TextField(null=True,blank=True)
    #queria agregarle titulo, pero creo esta demas
    #titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(null=False,blank=False)
    url_img = models.TextField(null=True,blank=True)
    #se crea con 0 y 0 al inicio
    like = models.ManyToManyField(Usuario, blank=True,related_name="likes")
    dislike = models.ManyToManyField(Usuario, blank=True,related_name="dislikes")
    confiable = models.BooleanField(default=False)


    #Por eliminar

    likes = models.IntegerField(default= 0)
    dislikes = models.IntegerField(default=0)

class Globales(models.Model):
    nombre = models.CharField(max_length=100,null=False,blank=True)
    global_py_var = models.IntegerField(default=1,null=True,blank=True)
