from django.urls import path
from . import views
from .views import manage_restaurant
from .views import cancel_reservation

urlpatterns = [
    path('restaurants/', views.list_restaurants, name='list_restaurants'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/reserve/', views.book_reservation, name='book_reservation'),
    path('restaurant/manage/<int:restaurant_id>/', manage_restaurant, name='manage_restaurant'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('profile/', views.user_profile, name='user_profile'),
]
