from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import EmailField, CharField
from django.forms.widgets import TextInput, PasswordInput


class UserCreationForm(UserCreationForm):
    '''
    Upgrade for adding email, first_name and last_name
    We can add 'help_text="Required.", '
    '''
    username = CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Your Username'}))
    email = EmailField(label="Email address", required=True, widget=TextInput(attrs={'placeholder': 'Email'}))
    first_name = CharField(max_length=30, widget=TextInput(attrs={'placeholder': 'First Name'}))
    last_name = CharField(max_length=30, widget=TextInput(attrs={'placeholder': 'Last Name'}))
    password1 = CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    password2 = CharField(widget=PasswordInput(attrs={'placeholder':'Repeat password'}))
    
    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name", "password1", "password2")

    def save(self, commit=True):
        '''
        Save the user
        '''
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        # user.is_active = False  # User automatically not active
        if commit:
            user.save()
        return user

class AuthenticationForm(AuthenticationForm):
    '''
    https://stackoverflow.com/questions/54152670/django-auth-add-placeholder-in-the-login-form/54152827
    '''
    username = CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Your Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
