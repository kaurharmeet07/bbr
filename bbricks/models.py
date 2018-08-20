from django.db import models
from django.contrib.auth.models import User
from time import time
from django.template.defaultfilters import slugify


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
    posted_by = models.CharField(max_length=10, choices=[('Owner', 'Owner'), ('Dealer', 'Dealer'), ('Builder', 'Builder')])
    project_name = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    area = models.IntegerField()
    units = models.CharField(max_length=50, choices=[('Marla', 'Marla'), ('Acres', 'Acres'), ('Sq.Ft.', 'Sq.Ft.')])
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.project_name


class Residential(Property):
    bedrooms = models.IntegerField()
    balconies = models.IntegerField()
    total_floors = models.IntegerField()
    age = models.IntegerField()
    parking = models.BooleanField()
    lift = models.BooleanField()
    park = models.BooleanField()
    power_backup = models.CharField(max_length=50, choices=[('None', 'None'), ('Full', 'Full'), ('Partial', 'Partial')])

    class Meta:
        abstract = True


class Apartment(Residential):
    property_on_floor = models.IntegerField()
    fire_alarm = models.BooleanField()

    def __str__(self):
        return self.project_name


class Villa(Residential):
    water_source = models.CharField(max_length=50, choices=[('Borewell/Tank', 'Borewell/Tank'),
                                                            ('Municipal Corporation', 'Municipal Corporation')])
    overlooking = models.CharField(max_length=50, choices=[('Main Road', 'Main Road'), ('Park', 'Park'),
                                                           ('Club', 'Club')], blank=True, null=True)

    def __str__(self):
        return self.project_name


class Land(Property):
    length = models.IntegerField()
    breadth = models.IntegerField()
    floors_allowed = models.IntegerField()
    registered = models.BooleanField()
    price_per_merla = models.IntegerField()
    boundary_wall = models.BooleanField()
    overlooking = models.CharField(max_length=50, choices=[('Main Road', 'Main Road'), ('Park', 'Park'),
                                                           ('Club', 'Club')], blank=True, null=True)

    def __str__(self):
        return self.project_name


class Sell(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('Apartment', 'Apartment'), ('Land', 'Land'),
                                                    ('Independent House', 'Independent House')])
    price = models.IntegerField()

    def __str__(self):
        return self.property.project_name


class Rent(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('Apartment', 'Apartment'), ('Land', 'Land'),
                                                    ('Independent House', 'Independent House')])
    rent_to = models.CharField(max_length=50, choices=[('Family', 'Family'), ('Single Men', 'Single Men'),
                                                       ('Single Women', 'Single Women')])
    available_from = models.DateField()
    furnishing = models.CharField(max_length=50, choices=[('Fully furnished', 'Fully furnished'),
                                                          ('Semi furnished', 'Semi furnished'),
                                                          ('Unfurnished', 'Unfurnished')])
    rent = models.IntegerField()
    security_deposit = models.IntegerField()

    def __str__(self):
        return self.property.project_name


class PayingGuest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('Apartment', 'Apartment'), ('Land', 'Land'),
                                                    ('Independent House', 'Independent House')])
    available_for = models.CharField(max_length=50, choices=[('Girls', 'Girls'), ('Boys', 'Boys'), ('Both', 'Both')])
    suitable_for = models.CharField(max_length=50, choices=[('Students', 'Students'), ('Professionals', 'Professionals')])
    available_from = models.DateField()
    furnishing = models.CharField(max_length=50, choices=[('Fully furnished', 'Fully furnished'),
                                                          ('Semi furnished', 'Semi furnished'),
                                                          ('Unfurnished', 'Unfurnished')])
    rent = models.IntegerField()
    security_deposit = models.IntegerField()

    def __str__(self):
        return self.property.project_name


def get_image_filename(instance, filename):
    title = instance.property.project_name
    slug = slugify(title)
    return "uploaded_files/%s-%s" % (slug, filename)


class Images(models.Model):
    property = models.ForeignKey(Property, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

    def __str__(self):
        return self.image
