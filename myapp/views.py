import email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Profile
from .forms import ProfilePhotoForm
from django.contrib.auth.decorators import login_required
from .forms import Contact
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta
from django.views.decorators import csrf
from .tempp import get_iternary
from django.http import HttpResponseServerError

def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime

def result(request):
    if request.method=='POST':
        print("post request success")
        destination = request.POST['destination']
        print(destination)
    return HttpResponse("hello")

from django.shortcuts import render
from django.utils import timezone

def travel_details(request):
    if request.method=='POST':
        context = {
        'destination': '{destination}',
        'start_date': timezone.now().date(),
        'end_date': timezone.now().date() + timezone.timedelta(days=5),
        'budget': '$2000',
        'days': 5,
        }
    return render(request, 'travel_details.html', context=context)

def demo(request):
    if request.method=='POST':
        destination = request.POST['destination']
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        min_budget = request.POST['max-budget']
        max_budget = request.POST['min-budget']
        print(destination)

        days = 3

        itinerary, summary, urls, start_date, end_date = get_iternary(destination, days, min_budget, max_budget)

        context = {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'min_budget': min_budget,
            'max_budget': max_budget,
            'itinerary': itinerary,
            'summary': summary,
            'urls': urls
        }


        return render(request, 'result.html',context=context)
        
     
    return render(request, 'demo.html')

def search_results(request):
    # Extract form data
    destination = request.GET.get('destination')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    budget = request.GET.get('budget')
    days = request.GET.get('days')

    # You can get the latitude and longitude from a database or some API for the selected destination
    lat = 38.5  # Example latitude
    lon = -78.5  # Example longitude
    weather_api_key = 'your_openweathermap_api_key'  # Put your API key here

    context = {
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date,
        'budget': budget,
        'days': days,
        'lat': lat,
        'lon': lon,
        'weather_api_key': weather_api_key,
    }

    return render(request, 'search.html', context)


def get_weather(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # OpenWeather API call
    API_KEY = 'your_openweathermap_api_key'
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&units=metric&cnt=16&appid={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    # Filter weather data
    filtered_forecast = [
        day for day in data['list']
        if start_date <= datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d') <= end_date
    ]

    return JsonResponse(filtered_forecast, safe=False)

def generate_itinerary(request):
    day_num = request.GET.get('day')
    destination = request.GET.get('destination')

    itinerary = f"""
    <h2>Day {day_num} in {destination}:</h2>
    <p><strong>08:00 AM:</strong> Start your day with breakfast.</p>
    <p><strong>10:00 AM:</strong> Visit an iconic location.</p>
    <p><strong>12:30 PM:</strong> Enjoy lunch at a popular spot.</p>
    <p><strong>02:30 PM:</strong> Explore more attractions.</p>
    <p><strong>05:00 PM:</strong> Relax at a scenic location.</p>
    <p><strong>07:00 PM:</strong> Dinner at a well-known restaurant.</p>
    """

    return JsonResponse({'itinerary': itinerary})

''''@login_required
def demo(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:demo')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'demo.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })
'''


@login_required
def search_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:search')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'search.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

def save_enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Save the form data to the database
        Contact.objects.create(name=name, email=email, message=message)

        send_mail(
            subject='Thank You for Your Query',
            message=f'Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you shortly.\n\nBest Regards,\nYour Company Name',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('blog:index')  # Redirect to the same page or a success page
    return render(request, 'index.html')  # For GET requests, just render the page

@login_required
def amristar_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:amristar')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'amristar.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })
    

@login_required
def agra_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:agra')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'agra.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

@login_required
def goa_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:goa')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'goa.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

@login_required
def kullu_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:kullu')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'kullu.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

@login_required
def pondicherry_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:pondicherry')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'pondicherry.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

@login_required
def andamanislands_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('blog:andamanislands')  # Redirect after successful upload to refresh the page
    else:
        form = ProfilePhotoForm(instance=profile)

    return render(request, 'andamanislands.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_email(email, otp):
    subject = 'Your OTP for Registration'
    message = f'Your OTP is {otp}. Please enter it to complete your registration.'
    send_mail(subject, message, 'noreply@example.com', [email])



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered')
                return redirect('blog:register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already registered')
                return redirect('blog:register')
            else:
                # Store user details in session
                request.session['username'] = username
                request.session['email'] = email
                request.session['password'] = password

                # Send OTP
                otp = generate_otp()  # Assume you have a function to generate OTP
                request.session['otp'] = otp

                # Send OTP to user's email (you would implement this)
                send_otp_via_email(email, otp)  # Replace with your email sending logic

                return redirect('blog:verify')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('blog:register')
    else:
        return render(request, 'register.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.info(request, 'User with this email does not exist')
            return redirect('blog:forgot_password')

        # Generate a random token (could also use OTP instead)
        reset_token = get_random_string(20)  # A random token to be sent to the user's email
        request.session['reset_token'] = reset_token
        request.session['reset_email'] = email

        # Send the reset token to the user's email
        subject = 'Password Reset Request'
        message = f'Your password reset token is {reset_token}. Use this token to reset your password.'
        send_mail(subject, message, 'noreply@example.com', [email])

        return redirect('blog:reset_password')

    return render(request, 'forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        token = request.POST['token']
        new_password = request.POST['password']
        confirm_password = request.POST['password2']

        # Validate token
        stored_token = request.session.get('reset_token')
        email = request.session.get('reset_email')

        if token == stored_token:
            if new_password == confirm_password:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()

                    # Clear session data after successful reset
                    del request.session['reset_token']
                    del request.session['reset_email']

                    messages.success(request, 'Password reset successfully. You can now log in with your new password.')
                    return redirect('blog:login')

                except User.DoesNotExist:
                    messages.info(request, 'User not found')
                    return redirect('blog:forgot_password')
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('blog:reset_password')
        else:
            messages.info(request, 'Invalid token')
            return redirect('blog:reset_password')

    return render(request, 'reset_password.html')


def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Get the user by email
        try:
            user = User.objects.get(email=email)
            username = user.username  # Get the associated username
        except User.DoesNotExist:
            messages.info(request, 'User with this email does not exist')
            return redirect('blog:login')

        # Authenticate using the username
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('blog:demo')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('blog:login')
    else:
        return render(request, 'login.html')

def verify(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            # Retrieve user details from session
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            # Check if the necessary details are present
            if username and email and password:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Clear session data
                del request.session['otp']
                del request.session['username']
                del request.session['email']
                del request.session['password']

                return redirect('blog:login')
            else:
                messages.info(request, 'User details are missing')
                return redirect('blog:register')
        else:
            messages.info(request, 'Invalid OTP')
            return redirect('blog:verify')
    else:
        return render(request, 'verify.html')
