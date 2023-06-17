from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import ft,Booking
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        Firstname = request.POST['Firstname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already used')
                return render('login')
            elif User.objects.filter(username=username).exists()            :
                messages.info(request,'username already used')
                return render('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return render(request,'login.html')
        else:
            messages.info(request,'Passwords are not matching')
            return redirect('register')
    else:
        return render(request,'register.html')

from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect, render

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username is an email
        if '@' in username:
            # User is trying to login with email
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # User is an admin
                auth.login(request, user)
                return redirect('/admin')
            else:
                # User is a customer
                auth.login(request, user)
                return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')  

def displayplanes(request):
    if request.method == 'POST':
        date_of_journey = request.POST.get('date_of_journey')
        source = request.POST.get('source')
        destination = request.POST.get('destination')

        fts = ft.objects.filter(
            date_of_journey=date_of_journey,
            source=source,
            destination=destination
        )

        context = {
            'fts': fts,
        }

        return render(request, 'displayplanes.html', context)

    return render(request, 'input.html')


def booking_view(request, ft_id):
    flight = get_object_or_404(ft, pk=ft_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        booking = Booking.objects.create(
            flight=ft
        )
    #return redirect('/')
    return render(request, 'booking.html', {'flight': flight})


def booking_history(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'booking_history.html', {'bookings': bookings})


