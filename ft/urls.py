from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name  = "home"),
    path('login',views.login, name = "login"),
    path('logout', views.logout, name = "logout"),
    path('register', views.register, name = "register"),
    path('booking/<int:ft_id>/', views.booking_view, name='booking'),
    path('booking/history/', views.booking_history, name='booking_history'),
    path('planes/', views.displayplanes, name='displayplanes'),
]
