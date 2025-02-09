from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'datetime', 'people', 'special_requests']
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 3}),
            'people': forms.Select(choices=Booking.CATEGORY_CHOICES, attrs={'class': 'form-select'}),
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
"""class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})
"""