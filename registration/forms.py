from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, CharField


class UserCreationForm(UserCreationForm):
    '''
    Upgrade for adding email, first_name and last_name
    '''
    email = EmailField(label="Email address", required=True, help_text="Required.")
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    
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
        if commit:
            user.save()
        return user


# ToDo: for upgrading login form: https://stackoverflow.com/questions/48814504/how-can-i-add-a-class-atribute-to-django-auth-login-form