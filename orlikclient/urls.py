from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register-view'),
    path('addUser/', views.register_user, name='register-user'),
    path('home/', views.home, name='home'),
    path('registerFailure/', views.register_failure, name='register-failure'),
    path('systemFailure/', views.system_failure, name='system-failure'),
    path('reservations/', views.reservations, name='reservations'),
    path('account/', views.account, name='account'),
    path('account/reset/', views.account_change_passwd, name='account-change-passwd'),
    path('account/delete/', views.account_delete, name='account-delete')
]
