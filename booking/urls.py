from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.list_restaurants, name='list_restaurants'),
    path('restaurants-detail/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants-form/', views.book_reservation, name='book_reservation'),
]
