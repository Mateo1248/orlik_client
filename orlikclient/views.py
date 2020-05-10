from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import RegisterData, Reservation
import requests
import json

BASE_ENDPOINT = 'http://localhost:5000'
REGISTER_ENDPOINT = BASE_ENDPOINT + '/users'
RESERVATIONS_ENDPOINT = BASE_ENDPOINT + '/reservations'

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


def register_view(request):
    return render(request, 'register.html')


def home(request):
    return render(request, 'home.html')


def register_failure(request):
    return render(request, 'registerFailure.html')


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
