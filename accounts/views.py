from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register_view(request):
    error = None
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        c = request.POST.get('confirm_pass')

        if p != c:
            error = "Passwords do not match. Try again."
        elif User.objects.filter(username=u).exists():
            error = "Username already taken. Try again."
        else:
            User.objects.create_user(username=u, password=p)
            return redirect('login')
    return render(request, 'accounts/register.html', {'error': error})


def login_view(request):
    error = None
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Inavlid username or password. Try again."
    return render(request, 'accounts/login.html', {'error': error})

def logout_view(request):
    # Clear active session user
    logout(request)
    return redirect('login')