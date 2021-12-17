from django.urls import path
from main import views
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
    path("lista/",views.rawListQuestion,name="pregunta-list"),#lista completa!
    path("confiable/",views.preguntaConfiable,name="pregConfiable"),#lista confiable!
    #path("pregunta/<int:question_id>/",views.singleQuestion,name="singleQuestion"),
    #path('listar', views.PreguntaListView.as_view(), name = 'pregunta-list'),
    path('crearPregunta/',views.PreguntaCreateView, name = 'pregunta-create'),
    path("crearRpta/<int:username>/<int:question_id>/",views.createReply,name="createReply"),
    path('table/<int:pk>/', views.PreguntaDetailView, name = 'pregunta-detail'),
]