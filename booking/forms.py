from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Restaurant
from django.forms import ModelForm, DateInput, TimeInput, Textarea, NumberInput, CharField, Select, IntegerField
from .models import Reservation
from .models import Review
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_people', 'special_requests']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
            'number_of_people': NumberInput(attrs={'min': 1, 'step': 1}),
            'special_requests': Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        input_date = self.cleaned_data['date']
        # Ensure the reservation is at least one day in the future
        if input_date <= date.today():
            raise ValidationError("Reservations must be made at least one day in advance.")
        return input_date

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Remove 'is_manager' from this list

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['code', 'name', 'address', 'city', 'tt', 'type', 'capacity', 'description']
        widgets = {
            'description': Textarea(attrs={'rows': 4, 'cols': 40}),
            'type': Select()
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isalnum():
            raise forms.ValidationError("Code must be alphanumeric.")
        return code

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 5}),
            'rating': Select(choices=[(i, str(i)) for i in range(1, 6)])
        }
