from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate


def login_view(request):
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)

       if form.is_valid():
           data = form.cleaned_data
           usuario = data.get('username')
           password = data.get('password')
           user = authenticate(username=usuario, password=password)
           # user puede ser un usuario o None
           if user:
               login(request=request, user=user)
               url_exitosa = reverse('inicio')
               return redirect(url_exitosa)
   else:  # GET
       form = AuthenticationForm()
   return render(
       request=request,
       template_name='perfiles/login.html',
       context={'form': form},
   )

class CustomLogoutView(LogoutView):
   template_name = 'perfiles/logout.html'