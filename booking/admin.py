from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Restaurant, Reservation
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(Restaurant)
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'date', 'time']
    list_filter = ['date', 'restaurant']
    search_fields = ['user__username', 'restaurant__name']
admin.site.register(User, UserAdmin)
