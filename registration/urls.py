from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from . import forms


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=forms.AuthenticationForm)),    # to add placeholder
    path('', include('django.contrib.auth.urls')),     # Auth
]

# ToDO: provare a fare il signup anche come il login
# ToDo: sovrascrivere le altre pagine di registration!