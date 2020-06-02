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
PITCHES_ENDPOINT = BASE_ENDPOINT + '/pitches'

token = ''
user = ''

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
    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }
    print("Request for all pitches")
    response = requests.get(PITCHES_ENDPOINT, headers=headers)

    pitches = []
    if response.status_code == 200:
        print("All pitches successfully listed")
        response_content = response.json()
        for pitch in response_content:
            pitches.append(
                Pitch(
                    id=pitch['pitchId'],
                    pitch_name=pitch['pitchName'],
                    coordinateX=pitch['latitude'],
                    coordinateY=pitch['longitude']
                )
            )
    else:
        print("Error while listing pitches", response.status_code)
        #     errorPage
        pass

    context = {
        'user_pitches': pitches
    }
    return render(request, 'templateMap.html', context)


def list_user_reservations(request):
    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }
    reservation_list = []
    response = requests.get(RESERVATIONS_ENDPOINT + user, headers=headers)
    if response.status_code == 200:
        for reservation in response.content:
            reservation_list.append(
                Reservation(
                    reservation_id=reservation['reservationId'],
                    date=reservation['reservationDate'],
                    start_hour=reservation['startHour'],
                    end_hour=reservation['endHour'],
                    pitch_name=reservation['pitchName'],
                )
            )
    context = {
        'user_reservations': reservation_list
    }
    return render(request, 'listUserReservations.html', context)


def make_reservation(request, pitch_id=None):
    selected_pitch_name = None
    selected_pitch_id = None
    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }
    response = requests.get(PITCHES_ENDPOINT, headers=headers)

    pitches = []
    if response.status_code == 200:
        response_content = response.json()
        for pitch in response_content:
            new_pitch = Pitch(
                id=pitch['pitchId'],
                pitch_name=pitch['pitchName'],
                coordinateX=pitch['latitude'],
                coordinateY=pitch['longitude']
            )
            if new_pitch.id != pitch_id:
                pitches.append(new_pitch)
            else:
                selected_pitch_name = new_pitch.pitch_name
                selected_pitch_id = new_pitch.id
    else:
        #     errorPage
        pass

    if selected_pitch_id is None:
        context = {
            'selected_pitch_id': pitches[0].id,
            'selected_pitch_name': pitches[0].pitch_name,
            'rest_pitches': pitches[1:]
        }
    else:
        context = {
            'selected_pitch_id': selected_pitch_id,
            'selected_pitch_name': selected_pitch_name,
            'rest_pitches': pitches
        }
    print(str(context))
    return render(request, 'makeReservation.html', context)


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

    headers = {
        'Content-type': 'application/json'
    }
    response = requests.post(LOGIN_ENDPOINT, data=json.dumps(login_data_dto), headers=headers)
    status_code = response.status_code
    if status_code == 200:
        token = response.headers.get('Authorization')
        user = login_data_dto['userLogin']
        return redirect('/home/')
    elif 400 <= status_code < 500:
        print(status_code)
        return redirect('/loginFailure/')
    else:
        return redirect('/systemFailure/')


def redirect_to_make_reservation(request):
    pitch_id = request.POST['id'],
    return make_reservation(request, int(pitch_id[0]))


def confirm_reservation(request):
    print(request.POST['date'], request.POST['start-hour'], request.POST['end-hour'], request.POST['pitch'])
    return list_user_reservations(request)
