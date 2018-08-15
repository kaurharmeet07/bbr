from django.db import models
from django.contrib.auth.models import User
from time import time


class State(models.Model):
    state_name = models.CharField(max_length=200)

    def __str__(self):
        return self.state_name


class City(models.Model):
    city_name = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to=get_upload_file_name)
    mobile_no = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Property(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    locality = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    bedrooms = models.IntegerField()
    area = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    photo = models.FileField(upload_to=get_upload_file_name)

    def __str__(self):
        return self.locality
