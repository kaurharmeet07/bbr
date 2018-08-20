from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import MyRegistrationForm, UserProfileForm, ImageForm, ApartmentForm
from .models import UserProfile, Apartment, Images
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
                                                       'properties': user.userprofile.property_set.all() })


def properties(request):
    args = {}
    args.update(csrf(request))
    args['properties'] = Property.objects.all()

    return render_to_response('bbricks/properties.html', args)


def property(request, property_id=1):
    return render(request, 'bbricks/property.html',
                  {'property': Apartment.objects.get(id=property_id)})


@login_required
def create_property(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=5)

    if request.POST:
        apartmentForm = ApartmentForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if apartmentForm.is_valid() and formset.is_valid():
            apartment_form = apartmentForm.save(commit=False)
            apartment_form.seller = request.user.userprofile
            apartment_form.save()

            for f in formset.cleaned_data:
                image = f['image']
                photo = Images(property=apartment_form, image=image)
                photo.save()

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

    return render_to_response('bbricks/property_create.html', args)


def sell(request):
    pass


def rent(request):
    pass


def pg(request):
    pass
