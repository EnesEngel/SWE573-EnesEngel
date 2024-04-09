from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.contrib.auth.hashers import make_password
# Create your views here.


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        password = request.POST.get('password')

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            is_private = form.cleaned_data['is_private']

            user = User.objects.create(
                username=username,
                email=email,
                password_hash=make_password(password),
                is_private=is_private
            )
            messages.success(request, 'User created successfully!')
            return redirect('home')
        else:
            err_str = ""
            for field in form:
                if field.errors:
                    err_str += field.name + " Already Exists.\n"
            messages.error(request, err_str)

    else:
        form = UserForm()
    return render(request, 'BoSApp/create_user.html', {'form': form})


def home(request):
    return render(request, 'BoSApp/home.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       # try:
        # user = User.objects.get(username=username)
        # flash messages gelecek ve user modeli eklenmeli
    context = {}
    return render(request, 'BoSApp/login_register.html', context)
