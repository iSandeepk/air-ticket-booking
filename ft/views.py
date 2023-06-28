from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import ft,Booking,UserProfile
from django.contrib.auth import authenticate,logout,login as auth_login
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.utils import timezone



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
                user_profile = UserProfile(user=user, Firstname=Firstname)
                user_profile.save()
                return redirect('login')
        else:
            messages.info(request,'Passwords are not matching')
            return redirect('register')
    else:
        return render(request,'register.html')


def login(request):
    session_timeout = getattr(settings, 'SESSION_COOKIE_AGE', 1800)  # Default: 30 minutes
    last_activity = request.session.get('last_activity')
    if last_activity is not None and (timezone.now() - last_activity).seconds > session_timeout:
        auth.logout(request)
        messages.info(request, 'You have been logged out due to inactivity.')
        return redirect('login')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                return redirect('/admin/')
            else:
                auth_login(request, user)
                subject = 'Login Notification'
                message = 'You have logged in to our website.'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = user.email
                
                send_mail(subject, message, from_email, [to_email])
                
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



from django.core.mail import EmailMessage
@login_required
def booking_view(request, ft_id):
    flight = get_object_or_404(ft, pk=ft_id)
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Send email to the user
        auth_login(request, request.user)
        subject = 'Booking Confirmation'
        message = "hello"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = request.user.email

        send_mail(subject, message, from_email, [to_email])
        # Reduce the number of seats
        if ft.seats_available > 0:
            ft.seats_available -= 1
            ft.save()

            success_message = 'Booking confirmed successfully.'
        else:
            success_message = 'Sorry, no seats available for booking.'

    return render(request, 'booking.html', {'flight': flight, 'success_message': success_message})





def booking_history(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'booking_history.html', {'bookings': bookings})

'''
def flight_fare_search(request):
    if request.method == 'POST':
        if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        adult = request.POST.get('adult')
        type = request.POST.get('type')
        
        url = "https://flight-fare-search.p.rapidapi.com/v2/flight/"
        querystring = {
        "from": source,
        "to": destination,
        "date": date,
        "adult": adult,
        "type": type,
        "currency": "USD"
        }
        headers = {
        "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
        "X-RapidAPI-Host": "flight-fare-search.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            fares = data.get('results', [])

            context = {'fares': fares}
            return render(request, 'fare_results.html', context)
        else:
            error_message = f"Error occurred: {response.status_code}"
            return render(request, 'error.html', {'error_message': error_message})
    else:
        return render(request, 'input.html')
'''

# trail done need to execute the main page
'''
def flight_fare_search(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        adult = request.POST.get('adult')
        type = request.POST.get('type')

    url = "https://flight-fare-search.p.rapidapi.com/v2/flight/"

    querystring = {
        "from": "VTZ",
        "to": "HYD",
        "date": "2023-06-22",
        "adult": "1",
        "type": "economy",
        "currency": "USD"
    }

    headers = {
        "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
        "X-RapidAPI-Host": "flight-fare-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        fares = data.get('results', [])

        context = {'fares': fares}
        return render(request, 'fare_results.html', context)
    else:
        error_message = f"Error occurred: {response.status_code}"
        return render(request, 'error.html', {'error_message': error_message})'''
'''
def airport_depature(request):
    if request.method == 'POST':
        name = request.POST.get(name)
        url = "https://flight-fare-search.p.rapidapi.com/v2/airport/departures"
        querystring = {"airportCode":"LHR"}

        headers = {
            "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
            "X-RapidAPI-Host": "flight-fare-search.p.rapidapi.com"
        }
        url = "https://skyscanner50.p.rapidapi.com/api/v1/searchFlights"

        querystring = {"origin":"LOND","destination":"NYCA","date":"<REQUIRED>","adults":"1","currency":"USD","countryCode":"US","market":"en-US"}

        headers = {
            "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
            "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            depatures = data.get('results', [])

            context = {'depatures': depatures}
            return render(request, 'depature_results.html', context)
        else:
            error_message = f"Error occurred: {response.status_code}"
            return render(request, 'error.html', {'error_message': error_message})
'''