from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Restaurant

class ReservationForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    number_of_people = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'step': '1'}))
    special_requests = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))



class CustomUserCreationForm(UserCreationForm):
    is_manager = forms.BooleanField(required=False, help_text='Check if registering as a restaurant manager.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_manager')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = self.cleaned_data['is_manager']
        if commit:
            user.save()
        return user

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'capacity', 'description']
