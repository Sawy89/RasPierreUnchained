from django.shortcuts import render
from . import models


def index(request, code='it'):
    request.is_free = True # login not needed, nut bar displayed
    
    # Text for my description
    text_list = models.Content.objects.filter(language=code).all()

    # Languages
    languages = models.Language.objects.all()

    return render(request, 'myself/index.html', {'text_list': text_list, 'languages': languages}) 
