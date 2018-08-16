from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import MyRegistrationForm, PropertyForm, UserProfileForm
from .models import UserProfile, Property
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
                  {'property': Property.objects.get(id=property_id)})


def create_property(request):
    if request.POST:
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.seller = request.user.userprofile
            f.save()

            return HttpResponseRedirect('/bbricks/loggedin')
    else:
        form = PropertyForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('bbricks/property_create.html', args)


