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
    url(r'^create/$', views.create),
    url(r'^get_apartment/(?P<apartment_id>\d+)/$', views.apartment),
    url(r'^get_house/(?P<house_id>\d+)/$', views.house),
    url(r'^get_land/(?P<land_id>\d+)/$', views.land),
    url(r'^create_apartment/$', views.create_apartment),
    url(r'^create_house/$', views.create_house),
    url(r'^create_land/$', views.create_land),
    url(r'^sell/(?P<property_id>\d+)/$', views.sell),
    url(r'^rent/(?P<property_id>\d+)/$', views.rent),
    url(r'^pg/(?P<property_id>\d+)/$', views.pg),
    url(r'^buy/$', views.buy),
    url(r'^buy_rent/$', views.buy_rent),
]
