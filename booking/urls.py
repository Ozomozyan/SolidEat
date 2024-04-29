from django.urls import path
from . import views
from .views import manage_restaurant, user_profile_public, edit_review, delete_review, cancel_reservation, edit_reservation, delete_reservation

urlpatterns = [
    path('restaurants/', views.list_restaurants, name='list_restaurants'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/reserve/', views.book_reservation, name='book_reservation'),
    path('restaurant/manage/<int:restaurant_id>/', manage_restaurant, name='manage_restaurant'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('user/<int:user_id>/', user_profile_public, name='user_profile_public'),
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('reservation/edit/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('reservation/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
]
