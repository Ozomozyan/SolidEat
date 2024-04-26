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
from .forms import ReservationForm, ReviewForm

def home(request):
    return render(request, 'home.html')

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        if 'reserve' in request.POST:
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reservation.user = request.user
                reservation.restaurant = restaurant
                reservation.save()
                messages.success(request, 'Reservation made successfully!')
                return redirect('restaurant_detail', restaurant_id=restaurant.id)
        elif 'review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.restaurant = restaurant
                review.save()
                messages.success(request, 'Review posted successfully!')
                return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        reservation_form = ReservationForm()
        review_form = ReviewForm()
    
    return render(request, 'booking/restaurant_detail.html', {
        'restaurant': restaurant,
        'reservation_form': reservation_form,
        'review_form': review_form
    })

def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'booking/list_restaurants.html', {'restaurants': restaurants})

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

@login_required
def user_profile(request):
    return render(request, 'booking/user_profile.html')

@login_required
def book_reservation(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            reservation.user = request.user
            reservation.save()
            # Redirect to a new URL, for example the restaurant detail page
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = ReservationForm()

    return render(request, 'booking/reservation_form.html', {'form': form, 'restaurant': restaurant})


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