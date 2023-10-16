from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from todo.models import Todo


# Create your views here.
def index(request):
    todo = None
    if request.user.is_authenticated:
        todo = Todo.objects.filter(user=request.user).all()

    if request.method == 'POST':
        new_todo = Todo(
            title=request.POST['title'],
            user=request.user
        )
        new_todo.save()
        messages.error(request, 'Tarea creada con éxito')
        return redirect('/')

    return render(request, 'index.html', {'todos': todo})


def delete(request, pk):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    messages.info(request, 'Tarea completada con éxito')
    return redirect('/')


# Registro

def user_signup(user, passw):
    user = User(username=user)

    user.set_password(passw)

    user.save()


# Login

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        exist = User.objects.filter(username=username).count()

        if not exist:
            user_signup(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, 'Bienvenido ' + request.user.username)
            return redirect('index')
        else:
            return redirect('login')

    return render(request, "login.html")


# Logout

def user_logout(request):
    logout(request)
    return redirect("login")
