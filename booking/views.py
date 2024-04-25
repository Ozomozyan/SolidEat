from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from .models import Restaurant, Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ReservationForm
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Restaurant
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required, user_passes_test

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_manager:
                group = Group.objects.get(name='Managers')
                user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
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


def manager_check(user):
    return user.is_authenticated and user.is_manager

@login_required
@user_passes_test(manager_check)
def manage_restaurant(request, restaurant_id):
    # Ensure the restaurant belongs to the logged-in manager
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, manager=request.user)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant details updated successfully!')
            return redirect('manage_restaurant', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'booking/manage_restaurant.html', {
        'form': form,
        'restaurant': restaurant
    })