from django.urls import path
from main import views
app_name="main"

urlpatterns=[
    path("confiable/",views.preguntaConfiable,name="pregConfiable"),
    path("<int:question_id>/",views.singleQuestion,name="singleQuestion"),
    path('listar', views.PreguntaListView.as_view(), name = 'pregunta-list'),
    path('crear/',views.PreguntaCreateView, name = 'pregunta-create'),
    path('table/<int:pk>/', views.PreguntaDetailView, name = 'pregunta-detail'),
]