from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model

from .models import Categoria, Pregunta, Usuario
User = get_user_model()

# Register your models here.
admin.site.register(User)
admin.site.register(Pregunta)
admin.site.register(Categoria)