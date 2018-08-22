from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Apartment, Sell, Images, Villa, Land, Rent, PayingGuest


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
        fields = ('posted_by', 'posted_for', 'project_name', 'state', 'city', 'locality', 'address',
                  'area', 'units', 'bedrooms', 'balconies', 'total_floors', 'property_on_floor',
                  'age', 'parking', 'lift', 'park', 'power_backup',
                  'fire_alarm', 'description', )


class HouseForm(forms.ModelForm):

    class Meta:
        model = Villa
        fields = ('posted_by', 'posted_for', 'project_name', 'state', 'city', 'locality', 'address',
                  'area', 'units', 'bedrooms', 'balconies', 'total_floors',
                  'age', 'parking', 'lift', 'park', 'power_backup',
                  'water_source', 'overlooking', 'description', )


class LandForm(forms.ModelForm):

    class Meta:
        model = Land
        fields = ('posted_by', 'project_name', 'state', 'city', 'locality', 'address',
                  'area', 'units', 'length', 'breadth', 'floors_allowed', 'registered',
                  'boundary_wall', 'overlooking', 'price_per_merla', 'description', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Images
        fields = ('image', )


class SellForm(forms.ModelForm):

    class Meta:
        model = Sell
        fields = ('price', )


class RentForm(forms.ModelForm):

    class Meta:
        model = Rent
        fields = ('rent_to', 'available_from', 'furnishing', 'rent', 'security_deposit')


class PGForm(forms.ModelForm):

    class Meta:
        model = PayingGuest
        fields = ('available_for', 'available_from', 'furnishing', 'suitable_for', 'rent', 'security_deposit')

