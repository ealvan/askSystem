from django.urls import path
from main import views
from .models import Globales

app_name="main"

#la vista mainPreguntas, se encargara de tener
# una interface para todas las preguntas, confiables no confiables, etc.

# op1)  "dos botones" para que te 
#       muestren las confiables y no confibles , o solo un boton

# op2) tener al buscador que busque de 
# aceurdo a sus filtros, y que te muestre resultados
# en otro template(opcion mas ligica y recomendable jeampier, busca el archivo
# rawListQuestion.html en templates/main/)

# op3) (no recomendable pero las mas facil jeampier)
#   Que exista un boton que te lleve al buscador, para buscar
#   esta template puede ser accedida por todos, 
#   solo para leer, pero no para eliminar y cosas crud
#   es decur a no usuarios tambien pueden ver todas 
#   las preguntas, pero no pueden editar ni eliminar nada

urlpatterns=[
]