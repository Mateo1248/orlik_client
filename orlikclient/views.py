from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import RegisterData
import requests
import json

# Create your views here.
REGISTER_USER_ENDPOINT = 'http://localhost:5000/users'


def register_view(request):
    return render(request, 'register.html')


def register_success(request):
    return render(request, 'registerSuccess.html')


def register_failure(request):
    return render(request, 'registerFailure.html')


def system_failure(request):
    return render(request, 'systemFailure.html')


def register_user(request):
    register_data = RegisterData(email=request.POST['email'], password=request.POST['password'])
    register_data_dto = {
        'userLogin': register_data.email,
        'userPassword': register_data.password
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(REGISTER_USER_ENDPOINT, data=json.dumps(register_data_dto), headers=headers)
    status_code = response.status_code
    if status_code == 201:
        return redirect('/registerSuccess/')
    elif 400 <= status_code < 500:
        return redirect('/registerFailure/')
    else:
        return redirect('/systemFailure/')
