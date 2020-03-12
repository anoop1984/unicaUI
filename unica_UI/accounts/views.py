from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import  auth
from django.contrib import messages
from pages import views

def register(reqeust):
    return render(reqeust, 'accounts/register.html')

def login(request):
    print("Inside login")
    if request.user.is_authenticated:
        print("user authenticted")
        return redirect(views.index2)

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print("user authenticating")
        user  = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(views.index2)
        else:
            messages.error(request, "Login Failed")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def login1(request):
    print("Inside login")
    if request.user.is_authenticated:
        print("user authenticted")
        return redirect(views.index2)

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print("user authenticating")
        user  = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(views.index2)
        else:
            messages.error(request, "Login Failed")
            return redirect('login')
    else:
        return render(request, 'accounts/login1.html')


def login2(request):
    print("Inside login")
    if request.user.is_authenticated:
        print("user authenticted")
        return redirect(views.index2)

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print("user authenticating")
        user  = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(views.index2)
        else:
            messages.error(request, "Login Failed")
            return redirect('login2')
    else:
        return render(request, 'accounts/login2.html')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request, 'accounts/login2.html')



def dashboard(request):
    return render(request, 'accounts/dashboard.html')
