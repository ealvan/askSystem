from django.urls import path
from . import views
app_name="account"

#la vista de loginlogout se encarga en administrar el ingreso y salida de las sesiones
#Login para iniciar sesion
#logout para cesar sesion

urlpatterns = [
	path("", views.login, name = "login"),
	path("logout/", views.logout, name = "logout"),
	path("home/",views.home,name="home"),
]
