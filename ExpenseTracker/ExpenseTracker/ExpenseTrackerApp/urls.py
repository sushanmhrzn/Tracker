from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('index/',views.index),
    path('signup/',views.signup,name='singup'),
    path('handlesignup/',views.handleSignup),
    path('handlelogin/',views.handleLogin)
]