"""askSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index, name="index"),
    path("question/",views.listQuestion, name="list"),
    path("question/<int:question_id>/",views.singleQuestion, name="question"),
    path("question/<int:question_id>/det/",views.PreguntaDetailView, name="detalles"),
    path('question/<int:pk>/delete/', views.PreguntaDeleteView.as_view(), name = 'pregunta-delete'),
    path('question/<int:pk>/update/', views.PreguntaUpdateView.as_view(), name = 'pregunta-update'),
    path("question/ask",views.PreguntaCreateView, name="ask"),
    path("reply/<int:username>/<int:question_id>/",views.createReply,name="reply"),
    path("search",views.resultados, name="search"),
    path("logout/", views.logout, name = "logout"),
    path("login/", views.login, name = "login"),
    path('createuser/', views.SignUp, name="SignUp"),
    #grafico
    path("question/<int:question_id>/grafico/",views.PreguntaGraficoView, name="pregunta-grafico"),
]
