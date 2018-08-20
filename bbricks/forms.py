from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Apartment, Villa, Images


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('mobile_no', 'photo')


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class ApartmentForm(forms.ModelForm):

    class Meta:
        model = Apartment
        fields = ('posted_by', 'project_name', 'state', 'city', 'locality', 'address',
                  'area', 'units', 'bedrooms', 'balconies', 'total_floors', 'property_on_floor',
                  'age', 'parking', 'lift', 'park', 'power_backup',
                  'fire_alarm', 'description', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Images
        fields = ('image', )
