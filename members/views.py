from . decorators import unauthenticated_user
from .forms import CreateUserForm
from custodia.models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import cache_page
from members.models import Modulos

# @unauthenticated_user
# def registerPage(request):
#     form = CreateUserForm()
#     if request.method=='POST':
#         form=CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request,'User created successfully for ' + user)
#             return redirect('login')
#     context = {'form':form}
#     return render(request,'register.html',context)

cache_page(60*5)
@login_required()
def homePage(request):
    usuarios = Profile.objects.get(user=request.user)
    return render(request,'index.html',{'usuarios':usuarios })
    
def loginPage(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'El usuario o la contraseña son incorrectos')
    context = {}
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')
    




