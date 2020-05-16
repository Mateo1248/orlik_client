from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register_or_login/', views.register_or_login_view, name='register_or_login_view'),
    path('addUser/', views.register_user, name='registerUser'),
    path('loginUser/', views.login_user, name='loginUser'),
    path('registerFailure/', views.register_failure, name='registerFailure'),
    path('loginFailure/', views.login_failure, name='loginFailure'),
    path('systemFailure/', views.system_failure, name='systemFailure'),
    path('listUserReservations/', views.list_user_reservations, name='listUserReservations'),
    path('makeReservation/', views.make_reservation, name='makeReservation'),
    path('account/', views.account, name='account'),
    path('account/change/', views.account_change_passwd, name='account-change-passwd'),
    path('account/delete/', views.account_delete, name='account-delete'),
]
