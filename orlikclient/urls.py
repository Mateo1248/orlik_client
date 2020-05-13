from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='registerView'),
    path('addUser/', views.register_user, name='registerUser'),
    path('home/', views.home, name='home'),
    path('registerFailure/', views.register_failure, name='registerFailure'),
    path('systemFailure/', views.system_failure, name='systemFailure'),
    path('listUserReservations/', views.list_user_reservations, name='listUserReservations'),
    path('makeReservation/', views.make_reservation, name='makeReservation')
]
