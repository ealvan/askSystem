from django.urls import path
from main import views
app_name="main"

urlpatterns=[
    path("",views.preguntaConfiable,name="pregConfiable"),
    path('listar', views.PreguntaListView.as_view(), name = 'pregunta-list'),
    path('crear/',views.PreguntaCreateView, name = 'pregunta-create'),
]