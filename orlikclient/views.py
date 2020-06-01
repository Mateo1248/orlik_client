from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from .models import RegisterData, Reservation, LoginData
from .models import RegisterData, Reservation, Pitch
import requests
import json

BASE_ENDPOINT = 'http://localhost:5000'
REGISTER_ENDPOINT = BASE_ENDPOINT + '/users'
LOGIN_ENDPOINT = BASE_ENDPOINT + '/login'
RESERVATIONS_ENDPOINT = BASE_ENDPOINT + '/reservations'
DELETE_USER_ENDPOINT = BASE_ENDPOINT + '/users/'
CHANGE_PASSWORD_ENDPOINT = BASE_ENDPOINT + '/users/'
MAP_ENDPOINT = BASE_ENDPOINT + '/map'

token = ''
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

user_pitches = [
    {

        'pitch_name': 'Orlik Spółdzielcza',
        'coordinateX': 17.0385,
        'coordinateY': 51.1059
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


def map(request):
    context = {
        'user_pitches': user_pitches
    }
    headers = {'Content-type': 'application/json'}
    response = requests.get(MAP_ENDPOINT + 'pilkarz1@gmail.com', headers=headers)
    print(response)
    pitches = []

    if response.status_code == 200:
        for pitch in response.content:
            print(pitch)
            pitches.append(
                Pitch(
                    pitch_name=pitch['pitchName'],
                    coordinateX=pitch['coordinateX'],
                    coordinateY=pitch['coordinateY']
                )
            )
    return render(request, 'templateMap.html', context)


def list_user_reservations(request):
    context = {
        'user_reservations': user_reservations
    }
    headers = {'Content-type': 'application/json'}
    reservation_list = []
    response = requests.get(RESERVATIONS_ENDPOINT + 'pilkarz1@gmail.com', headers=headers)
    print(response)
    # TODO to be changeed after implementing signing in
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
        return login_user(request)
    elif 400 <= status_code < 500:
        print(status_code)
        return redirect('/registerFailure/')
    else:
        return redirect('/systemFailure/')


def account(request):
    global user

    context = {
        'userLogin': user['userLogin'],
        'userPassword': user['userPassword']
    }

    return render(request, 'account.html', context)


def account_delete(request):
    global token
    global user

    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.delete(DELETE_USER_ENDPOINT + user['userLogin'], headers=headers)

    if response.status_code != 200:
        return redirect('/systemFailure/')

    return render(request, 'start.html')


def account_change_passwd(request):
    global token
    global user

    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    new_user_dto = {
        'userLogin': user['userLogin'],
        'userPassword': request.POST['new_password']
    }

    response = requests.patch(CHANGE_PASSWORD_ENDPOINT, data=json.dumps(new_user_dto), headers=headers)

    if response.status_code == 200:
        user = new_user_dto
    else:
        return redirect('/systemFailure/')

    return account(request)


def login_user(request):
    global token
    global user

    login_data = LoginData(email=request.POST['email'], password=request.POST['password'])
    login_data_dto = {
        'userLogin': login_data.email,
        'userPassword': login_data.password
    }

    headers = {'Content-type': 'application/json'}
    response = requests.post(LOGIN_ENDPOINT, data=json.dumps(login_data_dto), headers=headers)
    status_code = response.status_code
    if status_code == 200:
        token = response.headers.get('Authorization')
        user = login_data_dto
        return redirect('/home/')
    elif 400 <= status_code < 500:
        print(status_code)
        return redirect('/loginFailure/')
    else:
        return redirect('/systemFailure/')
