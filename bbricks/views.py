from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import MyRegistrationForm, UserProfileForm, ImageForm, ApartmentForm, SellForm
from .models import UserProfile, Apartment, Images, Property, Sell
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory


def home(request):
    return render_to_response('bbricks/home.html')


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('bbricks/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)

        try:
            check = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            check = None

        if check is not None:
            return HttpResponseRedirect('/bbricks/loggedin')
        else:
            return HttpResponseRedirect('/bbricks/editprofile')
    else:
        return HttpResponseRedirect('/bbricks/invalid')


@login_required
def loggedin(request):
    return render_to_response('bbricks/loggedin.html',
                              {'user': request.user,
                               'properties': request.user.userprofile.property_set.all()})


def invalid_login(request):
    return render_to_response('bbricks/invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('bbricks/logout.html')


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bbricks/register_success')

    args = {}
    args.update(csrf(request))

    args['form'] = MyRegistrationForm()

    return render_to_response('bbricks/register.html', args)


def register_success(request):
    return render_to_response('bbricks/register_success.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bbricks/loggedin')
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('bbricks/edit_profile.html', args)


def profile(request, username):
    user = User.objects.get(username=username)
    return render_to_response('bbricks/profile.html', {'user': user,
                                                       'properties': user.userprofile.property_set.all()})


def apartment(request, apartment_id=1):
    a = Apartment.objects.get(id=apartment_id)
    p = None
    if a.posted_for.__eq__('Sale'):
        p = Sell.objects.get(property=Property.objects.get(id=a.id))
    return render(request, 'bbricks/apartment.html',
                  {'apartment': a,
                   'p': p})


def house(request, house_id=1):
    pass


def land(request, land_id=1):
    pass


def create(request):
    if request.method == 'POST':
        t = request.POST.get('type')
        return HttpResponseRedirect('/bbricks/create_%s' % t)
    else:
        args = {}
        args.update(csrf(request))
        return render_to_response('bbricks/create.html', args)


@login_required
def create_apartment(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=2)

    if request.POST:
        apartmentForm = ApartmentForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if apartmentForm.is_valid() and formset.is_valid():
            apartment_form = apartmentForm.save(commit=False)
            apartment_form.seller = request.user.userprofile
            apartment_form.type = 'Apartment'
            apartment_form.save()

            for f in formset.cleaned_data:
                image = f['image']
                photo = Images(property=apartment_form, image=image)
                photo.save()

            if apartment_form.posted_for == 'Sale':
                return HttpResponseRedirect('/bbricks/sell/%s' % apartment_form.id)
            else:
                return HttpResponseRedirect('/bbricks/loggedin')
        else:
            print(apartmentForm.errors, formset.errors)
    else:
        apartmentForm = ApartmentForm()
        formset = ImageFormSet(queryset=Images.objects.none())

    args = {}
    args.update(csrf(request))
    args['apartmentForm'] = apartmentForm
    args['formset'] = formset

    return render_to_response('bbricks/create_apartment.html', args)


def create_house(request):
    pass


def create_land(request):
    pass


def sell(request, property_id):
    if property_id:
        p = Property.objects.get(id=property_id)
        if request.POST:
            form = SellForm(request.POST)
            if form.is_valid():
                s = form.save(commit=False)
                s.property = p
                s.save()

                return HttpResponseRedirect('/bbricks/get_apartment/%s' % property_id)

        else:
            form = SellForm()

        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['property'] = p
        return render_to_response('bbricks/sell.html', args)


def rent(request):
    pass


def pg(request):
    pass


def buy_sell(request):
    args = {}
    args.update(csrf(request))
    args['apartments'] = Sell.objects.filter(property__posted_for='Sale', property__type='Apartment')
    args['houses'] = Sell.objects.filter(property__posted_for='Sale', property__type='Independent House')
    args['lands'] = Sell.objects.filter(property__posted_for='Sale', property__type='Land')

    return render_to_response('bbricks/properties.html', args)


def buy_rent(request):
    pass


def buy_pg(request):
    pass


def properties(request):
    args = {}
    args.update(csrf(request))
    args['properties'] = Property.objects.all()

    return render_to_response('bbricks/all.html', args)
