from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from .models import RegisterData, Reservation, LoginData
import requests
import json

BASE_ENDPOINT = 'http://localhost:5000'
REGISTER_ENDPOINT = BASE_ENDPOINT + '/users'
LOGIN_ENDPOINT = BASE_ENDPOINT + '/login'
RESERVATIONS_ENDPOINT = BASE_ENDPOINT + '/reservations'

token = 'token'

DELETE_USER_ENDPOINT = BASE_ENDPOINT + '/' #Delete
CHANGE_PASSWORD_ENDPOINT = BASE_ENDPOINT #Patch

token = 'token'
user = {}

user_reservations = [
    {
        'date': '2020-05-20',
        'start_hour': '10:00',
        'end_hour': '11:30',
        'pitch_name': 'Orlik Spółdzielcza',
        'reservation_id': '1'
    },
    {
        'date': '2020-05-21',
        'start_hour': '11:00',
        'end_hour': '12:30',
        'pitch_name': 'Orlik Dembowskiego',
        'reservation_id': '2'
    }
]    


def register_or_login_view(request):
    return render(request, 'start.html')


def home(request):
    return render(request, 'home.html')


def register_failure(request):
    return render(request, 'registerFailure.html')


def login_failure(request):
    return render(request, 'loginFailure.html')


def system_failure(request):
    return render(request, 'systemFailure.html')


def list_user_reservations(request):
    context = {
        'user_reservations': user_reservations
    }
    headers = {'Content-type': 'application/json'}
    reservation_list = []
    response = requests.get(RESERVATIONS_ENDPOINT + 'pilkarz1@gmail.com', headers=headers)
    print(response)
    #TODO to be changeed after implementing signing in
    if response.status_code == 200:
        for reservation in response.content:
            print(reservation)
            reservation_list.append(
                Reservation(
                    reservation_id=reservation['reservationId'],
                    date=reservation['reservationDate'],
                    start_hour=reservation['startHour'],
                    end_hour=reservation['endHour'],
                    pitch_name=reservation['pitchName'],
                )
            )
    return render(request, 'listUserReservations.html', context)


def make_reservation(request):
    return render(request, 'makeReservation.html')


def register_user(request):
    register_data = RegisterData(email=request.POST['email'], password=request.POST['password'])
    register_data_dto = {
        'userLogin': register_data.email,
        'userPassword': register_data.password
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(REGISTER_ENDPOINT, data=json.dumps(register_data_dto), headers=headers)
    status_code = response.status_code
    if status_code == 201:
        return redirect('/home/')
    elif 400 <= status_code < 500:
        print(status_code)
        return redirect('/registerFailure/')
    else:
        return redirect('/systemFailure/')


def account(request):
    context = {
        'userLogin': 'test@test.com',
        'userPassword': 'password'
    }

    if "show_password" not in request.GET:
        user_password = "".join(["*" for _ in range(len(user_password))])

    return render(request, 'account.html', context )


def account_delete(request):
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'token {}'.format(token)
    }

    response = requests.delete(DELETE_USER_ENDPOINT + user['email'], headers=headers)

    if response.status_code == 200:
        print("@@@@ usunięto")

    return render(request, 'register.html')


def account_change_passwd(request):
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'token {}'.format(token)
    }

    new_user_dto = {
        'userLogin': user['login'],
        'userPassword': request.POST['password']
    }

    response = requests.patch(DELETE_USER_ENDPOINT, data=json.dumps(login_data_dto), headers=headers)

    if response.status_code == 200:
        print("@@@@ zmieniono")

    return account(request)


def login_user(request):
    global token
    login_data = LoginData(email=request.POST['email'], password=request.POST['password'])
    login_data_dto = {
        'userLogin': login_data.email,
        'userPassword': login_data.password
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(LOGIN_ENDPOINT, data=json.dumps(login_data_dto), headers=headers)
    status_code = response.status_code
    token = response.headers.get('Authorization')
    if status_code == 200:
        return redirect('/home/')
    elif 400 <= status_code < 500:
        print(status_code)
        return redirect('/loginFailure/')
    else:
        return redirect('/systemFailure/')
