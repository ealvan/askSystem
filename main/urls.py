from django.urls import path
from main import views
app_name="main"

urlpatterns=[
    path("",views.preguntaConfiable,name="pregConfiable"),
    path("<int:question_id>/",views.singleQuestion,name="singleQuestion"),

]