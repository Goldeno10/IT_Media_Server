from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm


def registration_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('media:home')
        else:
            messages.error(request, 'Invalid registration details. Please try again.')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    """ Login a user """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('media:home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html') 

def logout_view(request):
    """ Logout a user """
    logout(request)
    return redirect('media:home')
