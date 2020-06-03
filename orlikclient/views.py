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
USER_RESERVATIONS_ENDPOINT = BASE_ENDPOINT + '/reservations/users'
DELETE_USER_ENDPOINT = BASE_ENDPOINT + '/users/'
CHANGE_PASSWORD_ENDPOINT = BASE_ENDPOINT + '/users/'
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


def start(request):
    global token
    token = ''
    return render(request, 'start.html')


def home(request):
    return render(request, 'home.html')


def register_failure(request):
    return render(request, 'registerFailure.html')


def login_failure(request):
    return render(request, 'loginFailure.html')


def system_failure(request):
    return render(request, 'systemFailure.html')


def show_map(request):
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
    pitch_names = []
    print("Listing user reservations", user)
    response = requests.get(USER_RESERVATIONS_ENDPOINT + "/" + user, headers=headers)
    if response.status_code == 200:
        print("Reservation successfully listed")
        for reservation in response.json():
            reservation_list.append(
                Reservation(
                    reservation_id=reservation['reservationId'],
                    date=reservation['reservationDate'],
                    start_hour=reservation['startHour'],
                    end_hour=reservation['endHour'],
                    pitch_id=reservation['whichPitch'],
                )
            )

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

        pitch_names = {pitch.id: pitch.pitch_name for pitch in pitches}

        for reservation in reservation_list:
            reservation.pitch_name = pitch_names[reservation.pitch_id]
    else:
        print("Error occurred while listing user reservations", response.status_code)
    context = {
        'user_reservations': reservation_list
    }
    return render(request, 'listUserReservations.html', context)


def make_reservation(request):
    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }

    date = request.POST['date']
    start_hour = request.POST['start-hour']
    end_hour = request.POST['end-hour']
    pitch_id = request.POST['pitch_id']

    request_body = {
        "reservationDate": date,
        "startHour": start_hour,
        "endHour": end_hour,
        "whichUser": user,
        "whichPitch": pitch_id
    }

    print("Sending request for make reservation")
    response = requests.post(RESERVATIONS_ENDPOINT, headers=headers, data=json.dumps(request_body))

    if 300 > response.status_code >= 200:
        print("Reservation successfully created", response.status_code)
    else:
        print("Error while making reservation", response.status_code)

    return list_user_reservations(request)


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


def account(request, password_changed=False):
    global user

    context = {
        'userLogin': user,
        'passwordChanged': password_changed
    }

    return render(request, 'account.html', context)


def account_delete(request):
    global token
    global user

    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }

    print("Deleting an account...")
    response = requests.delete(DELETE_USER_ENDPOINT + user, headers=headers)

    if response.status_code != 200:
        print("Error occurred while deleting account", response.status_code)
        return redirect('/systemFailure/')

    print("Account deleted successfully")
    return render(request, 'start.html')


def account_change_password(request):
    global token
    global user

    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }
    new_user_dto = {
        'userLogin': user,
        'userPassword': request.POST['new_password']
    }

    print("Requesting password change...")
    response = requests.patch(CHANGE_PASSWORD_ENDPOINT, data=json.dumps(new_user_dto), headers=headers)

    if response.status_code == 200:
        token = requests.post(LOGIN_ENDPOINT, data=json.dumps(new_user_dto), headers=headers)\
            .headers.get('Authorization')
        password_changed = True
        print("Password successfully changed")
    else:
        print("Error occurred when changing password. Error code", response.status_code)
        return redirect('/systemFailure/')

    return account(request, password_changed)


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

    print("Signing in...")
    response = requests.post(LOGIN_ENDPOINT, data=json.dumps(login_data_dto), headers=headers)
    status_code = response.status_code
    if status_code == 200:
        print("User signed in successfully")
        token = response.headers.get('Authorization')
        user = login_data_dto['userLogin']
        return redirect('/home/')
    elif 400 <= status_code < 500:
        print("Error occurred while signing in", status_code)
        return redirect('/loginFailure/')
    else:
        return redirect('/systemFailure/')


def confirm_reservation(request):
    print(request.POST['date'], request.POST['start-hour'], request.POST['end-hour'], request.POST['pitch'])
    return list_user_reservations(request)
