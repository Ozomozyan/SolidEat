from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Restaurant, Reservation
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(User, UserAdmin)
