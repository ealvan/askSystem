from django.urls import path
from main import views
app_name="main"

urlpatterns=[
    path("",views.preguntaConfiable,name="pregConfiable"),
    path('', views.PreguntaListView.as_view(), name = 'pregunta-list'),
]