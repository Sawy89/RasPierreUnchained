from django.shortcuts import render
from . import models


def index(request):
    request.is_free = True # login not needed, nut bar displayed
    
    # Text for my description
    text_list = models.Content.objects.filter(language='it').all()
    # text_list.append({'id': 'intro', 'title': "Who am I", 
    #             'text_short': 'ciao ciao',
    #             'text_all': "I'm a biomedical engineer, with some year of experience, interested in the biomedical field but also in the more general engineering. I'm a young guy searching the possibility to obtain new skills and new knowledge. I'v learned in my life hot to work in a team, obtaining the best results for me and my colleagues. In my first working experiences, I've been in very interesting and dynamic places, working with people from different country, improving my communicative skills and my technical knowledge. I've done many voluntary experience, and I like music, playing some instruments. "})
    
    # text_list.append({'id': 'Study', 'title': "Learning", 
    #             'text_short': 'Liceo Scientifico',
    #             'text_all': "I got my high school scientific diploma in 2008, with vote 100/100. Those 5 years had started like a game, I had known some people, I started to understand what learning was like. But what I learned was that I needed to work with other people to get things done, and that I have to be serious and take my responsability. My high school years teached me mainly a method of studying, that helped me in university, and they gave me some friends that I keep now!"})

    return render(request, 'myself/index.html', {'text_list': text_list}) 
