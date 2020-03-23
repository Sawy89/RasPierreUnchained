from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm


def signup(request):
    '''
    https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    https://stackoverflow.com/questions/7910769/extending-usercreationform-to-include-email-first-name-and-last-name
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})