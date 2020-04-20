# Project final

Web Programming with Python and JavaScript - Final Project

## Install
- Install Docker
- Run (in the main folder) `docker-compose build` and then `docker-compose up` (the command `python manage.py runserver` is inside the docker-compose commands)
--> you can do it easily by running the file `start.bat`
- Access to the shell inside docker: `docker exec -it container_name /bin/bash`
- Run `python manage.py makemigrations` (this is always manual, to let the user know something changed) and then `python mangage.py migrate` (this has been add to docker-compose), the first time, and every time there has been a change in code to `models.py`

- To access the shell: `python manage.py shell`
- To create admin: `python manage.py createsuperuser`


## Import data


## Configuration & Launch program
Set those ENV variable in the system before launching docker:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=yourmail
EMAIL_HOST_PASSWORD=yourpass!
```


## Program description
The project is solved with Django and Javascript.
The idea is to solve a real world problem: with my group of friends, for Christmas, we randomly select who is going to give a present to who --> everybody is going to receive a present from a random person; the idea is that 1 big gift is better than many little gift!
The project is a platform where user can subscribe, selecting to participate in a "house", and there they will be randomly assigned a gift to be done to another user.


### File description

### Biblio
- Login template: https://codepen.io/colorlib/pen/rxddKy
- Login overwrite: https://learndjango.com/tutorials/django-password-reset-tutorial, 
https://stackoverflow.com/questions/53563534/template-password-reset-form-html-does-not-overwrite-the-django-admin-template
- SocketIO: https://channels.readthedocs.io/en/latest/tutorial/part_1.html
- CSRF: https://docs.djangoproject.com/en/3.0/ref/csrf/
- AJAX: https://zerowithdot.com/django-2-ajax-call/, http://musings.tinbrain.net/blog/2015/aug/28/vanilla-js-meets-djangos-csrf/
- Event scheduler: https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6, https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html

### Note
Pay attention to date!
Data are store in DB as UTC=0, Italy is UTC=+1 (CET), but in winter is +2 (CEST) because of daylight