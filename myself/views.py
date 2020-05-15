from django.shortcuts import render


def index(request):
    request.is_free = True
    testo = {}
    testo['intro'] = "I'm a biomedical engineer, with some year of experience, interested in the biomedical field but also in the more general engineering. I'm a young guy searching the possibility to obtain new skills and new knowledge. I'v learned in my life hot to work in a team, obtaining the best results for me and my colleagues. In my first working experiences, I've been in very interesting and dynamic places, working with people from different country, improving my communicative skills and my technical knowledge. I've done many voluntary experience, and I like music, playing some instruments. "
    print(testo['intro'])
    return render(request, 'myself/index.html', {'testo': testo}) 
