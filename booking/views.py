from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Restaurant, Reservation

def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'booking/list_restaurants.html', {'restaurants': restaurants})
