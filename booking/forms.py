from django import forms
from django.forms import widgets

class ReservationForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    number_of_people = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'step': '1'}))
    special_requests = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
