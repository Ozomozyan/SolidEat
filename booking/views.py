from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from .models import Restaurant, Reservation, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, login
from .forms import ReservationForm
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Restaurant
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ReservationForm, ReviewForm
from datetime import date, datetime, timedelta


def home(request):
    return render(request, 'home.html')

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reservation_form = ReservationForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        if 'submit_reservation' in request.POST:
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reservation.user = request.user
                reservation.restaurant = restaurant
                reservation.save()
                messages.success(request, 'Reservation made successfully!')
                return redirect('restaurant_detail', restaurant_id=restaurant.id)
            else:
                messages.error(request, 'Reservation form is invalid.')
        elif 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.restaurant = restaurant
                review.save()
                messages.success(request, 'Review posted successfully!')
                return redirect('restaurant_detail', restaurant_id=restaurant.id)
            else:
                messages.error(request, 'Review form is invalid.')

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
    # Fetching additional data related to the user
    reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    reviews = Review.objects.filter(user=request.user).order_by('-date_posted')

    context = {
        'user': request.user,
        'reservations': reservations,
        'reviews': reviews,
        'today': date.today(),
    }
    return render(request, 'booking/user_profile.html', context)



@login_required
def book_reservation(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Start by creating a reservation instance from the form, but don't save it yet
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            reservation.user = request.user

            # Check current reservations to ensure capacity is not exceeded
            reservation_start_time = datetime.combine(reservation.date, reservation.time)
            reservation_end_time = reservation_start_time + timedelta(hours=3)  # Define how long a reservation blocks capacity

            # Fetch reservations that overlap this timeframe
            overlapping_reservations = Reservation.objects.filter(
                restaurant=restaurant,
                date=reservation.date,
                time__range=(reservation.time, (reservation_end_time - timedelta(seconds=1)).time()),
                is_active=True
            )

            current_capacity = sum(r.number_of_people for r in overlapping_reservations)
            if current_capacity + reservation.number_of_people > restaurant.capacity:
                messages.error(request, "Unable to book reservation due to capacity limits.")
                return render(request, 'booking/reservation_form.html', {'form': form, 'restaurant': restaurant})

            # Save reservation if capacity checks pass
            reservation.save()
            messages.success(request, 'Reservation made successfully!')
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
        else:
            messages.error(request, "There was a problem with your reservation form.")
    else:
        form = ReservationForm()

    return render(request, 'booking/reservation_form.html', {'form': form, 'restaurant': restaurant})



def manager_check(user):
    return user.is_authenticated and user.is_manager

@login_required
@user_passes_test(manager_check)
def manage_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, manager=request.user)  # Ensure only the manager can access
    form = RestaurantForm(request.POST or None, instance=restaurant)

    if request.method == 'POST' and 'update_restaurant' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant details updated successfully!')
            return redirect('manage_restaurant', restaurant_id=restaurant.id)

    reservations = Reservation.objects.filter(restaurant=restaurant).order_by('date')

    return render(request, 'booking/manage_restaurant.html', {
        'restaurant': restaurant,
        'form': form,
        'reservations': reservations,
    })
    
    
@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, restaurant__manager=request.user)
    form = ReservationForm(request.POST or None, instance=reservation)
    if form.is_valid():
        form.save()
        messages.success(request, 'Reservation updated successfully!')
        return redirect('manage_restaurant', restaurant_id=reservation.restaurant.id)
    return render(request, 'booking/edit_reservation.html', {'form': form})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, restaurant__manager=request.user)
    restaurant_id = reservation.restaurant.id
    reservation.delete()
    messages.success(request, 'Reservation deleted successfully!')
    return redirect('manage_restaurant', restaurant_id=restaurant_id)

    
@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if reservation.date > date.today():
        reservation.delete()  # This will completely remove the reservation from the database
        messages.success(request, "Your reservation has been successfully deleted.")
    else:
        messages.error(request, "Past reservations cannot be cancelled or deleted.")
    return redirect('user_profile')


User = get_user_model()  # Correct way to get the User model

@login_required
def user_profile_public(request, user_id):
    user_profile = get_object_or_404(User, pk=user_id)  # Now correctly using the custom User model
    reservations = Reservation.objects.filter(user=user_profile).order_by('-date')
    reviews = Review.objects.filter(user=user_profile).order_by('-date_posted')
    context = {
        'user': user_profile,
        'reservations': reservations,
        'reviews': reviews,
        'today': date.today(),
    }
    return render(request, 'booking/user_profile_public.html', context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensures that users can only edit their own reviews
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('restaurant_detail', restaurant_id=review.restaurant.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'booking/edit_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensures that users can only delete their own reviews
    restaurant_id = review.restaurant.id
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('restaurant_detail', restaurant_id=restaurant_id)
