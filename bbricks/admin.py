from django.contrib import admin
from .models import UserProfile, State, City, Property, Apartment, Land, Villa, PayingGuest, Rent, Sell, Images


admin.site.register(UserProfile)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Property)
admin.site.register(Land)
admin.site.register(Villa)
admin.site.register(PayingGuest)
admin.site.register(Rent)
admin.site.register(Apartment)
admin.site.register(Sell)
admin.site.register(Images)
