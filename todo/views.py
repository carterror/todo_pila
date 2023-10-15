from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from todo.models import Todo


# Create your views here.
def index(request):
    todo = Todo.objects.all()

    if request.method == 'POST':
        new_todo = Todo(
            title=request.POST['title'],
            user=request.user
        )
        new_todo.save()
        return redirect('/')

    return render(request, 'index.html', {'todos': todo})


def delete(request, pk):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    return redirect('/')


# Registro

def user_signup(request):
    user_signup_form = UserSignUpForm(request.POST)
    if user_signup_form.is_valid():
        user_signup_form.save()
        return render(request, "accounts/signup_success.html",
                      {"user": user_signup_form.cleaned_data.get("username")})

    return render(request, "accounts/signup.html", {"form": user_signup_form})


# Login

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        exist = User.objects.filter(username=username).count()

        user = authenticate(request, username=username, password=password)

        if not exist:
            return HttpResponse('mal')
        return HttpResponse('bien')

        if user is not None:
            login(request, user)
            return render(request, "index.html", {})
        else:
            return render(request, "login.html")

    return render(request, "login.html")


# Logout

def user_logout(request):
    logout(request)
    return redirect("login")
