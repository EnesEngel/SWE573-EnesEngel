from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'BoSApp/home.html')

def loginPage(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        #flash messages gelecek ve user modeli eklenmeli
    context={}
    return render(request, 'BoSApp/login_register.html', context)