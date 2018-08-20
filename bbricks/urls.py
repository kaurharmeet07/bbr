from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('editprofile/', views.user_profile),
    path('login/', views.login),
    path('auth/', views.auth_view),
    path('logout/', views.logout),
    path('loggedin/', views.loggedin),
    path('invalid/', views.invalid_login),
    path('register/', views.register_user),
    path('register_success/', views.register_success),
    url(r'^profile/(?P<username>\w+)/$', views.profile),
    url(r'^all/$', views.properties),
    url(r'^get/(?P<property_id>\d+)/$', views.property),
    url(r'^create/$', views.create_property),
    url(r'^sell/$', views.sell),
    url(r'^rent/$', views.rent),
    url(r'^pg/$', views.pg),
]
