from django.urls import path
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
]
