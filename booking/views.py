from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from .models import Restaurant, Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ReservationForm

def home(request):
    return render(request, 'home.html')

def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'booking/list_restaurants.html', {'restaurants': restaurants})

def restaurant_detail(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'booking/restaurant_detail.html', {'restaurants': restaurants})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def book_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Process the valid form data
            return redirect('success_url')  # Redirect to a new URL
    else:
        form = ReservationForm()
    return render(request, 'booking/reservation_form.html', {'form': form})