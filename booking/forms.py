from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Restaurant
from django.forms import ModelForm, DateInput, TimeInput, Textarea, NumberInput, CharField, Select, IntegerField
from .models import Reservation
from .models import Review
from django.contrib.auth.models import Group

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



class CustomUserCreationForm(UserCreationForm):
    is_manager = forms.BooleanField(required=False, help_text='Check if registering as a restaurant manager.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_manager']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = self.cleaned_data['is_manager']
        if user.is_manager:
            # Optionally assign the user to a group based on their role
            group, _ = Group.objects.get_or_create(name='Managers')
            user.save()
            user.groups.add(group)
        else:
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
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 5}),
        }