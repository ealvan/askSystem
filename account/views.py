from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout as do_logout


# Create your views here.
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request, user)
			return redirect('home/')
		else:
			messages.info(request, 'Datos incorrectos')
			return redirect('/login/')
	else:
		return render(request, 'login.html')
def home(request):
    return render(request, 'home.html')

def logout(request):
	#auth.logout(request)
	do_logout(request)
	return redirect('/login/home/')
