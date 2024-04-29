from django.contrib import admin
from .models import Restaurant, Reservation, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Custom admin for Restaurants to allow assigning managers
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager')
    search_fields = ('name', 'manager__username')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = User.objects.filter(is_manager=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Custom admin for Reservations to display more details
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'date', 'time']
    list_filter = ['date', 'restaurant']
    search_fields = ['user__username', 'restaurant__name']

# Custom User Admin to include is_manager field
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_manager',)}),  # Add 'is_manager' field to admin
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('is_manager',)}),
    )

# Register models with their respective admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)  # Now using the custom admin class
