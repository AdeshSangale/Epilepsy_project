from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required,user_passes_test

def index(request):
    return render(request,"index.html")

def register(request):
    if request.method == 'POST':  
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



      
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('predict')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def predict(request):
    return render(request,'predict.html')

def about(request):
    return render(request,'about.html')

def Precautions(request):
    return render(request,'Precautions.html')
def result(request):
    if request.method == 'POST':
        dfa = request.POST['dfa']
        hfd = request.POST['hfd']
        SVD_Entropy = request.POST['SVD_Entropy']
        Fisher_info = request.POST['Fisher_info']
        pfd = request.POST['pfd']
        
        lis = [dfa,hfd,SVD_Entropy,Fisher_info,pfd]
        print(lis)
        # Traning model
        from joblib import load
        model=load(r'C:\Users\GAURI\Downloads\Epilipecy Web   100% updated Code (1)\Epilipecy Web   100% updated Code\Epilepsy_project\model.joblib')
        
        # Make prediction
        result = model.predict([lis])
        print(result)

        if result[0]==0:
            print("Yes")
            value = 'Transition'

        elif result[0]==1:
            print("NO")
            value = 'Healthy'
                 
        else:
            print("Yes")
            value = 'Seizures'


    return render(request,'result.html',  {
                    'ans': value,
                    'title': 'Predict',
                 
                    
                })

login_required(login_url='login_view')



def display_csv(request):
    csv_file_path = "D:\Epilipecy Web\Epilepsy_project\Epilepsy_App\FCM_B.csv"
    
    data = []
    headers = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the first row as headers
        for row in reader:
            data.append(row)
    
    return render(request, 'display_csv.html', {'headers': headers, 'data': data})