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
Some testing data are imported with fixture data.json


## Configuration & Launch program
Set those ENV variable in the system before launching docker:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=yourmail
EMAIL_HOST_PASSWORD=yourpass!
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
```


## Program description
The project is solved with Django and Javascript and SQL.
The idea is to solve a real world problem: with my group of friends, for Christmas, we randomly select who is going to give a present to who --> everybody is going to receive a present from a random person; the idea is that 1 big gift is better than many little gift! Ex. Marco to Denny; Denny to Luca; Luca to Marco!
The project is a platform where users can subscribe, selecting to participate in a "room/house", and there they will be randomly assigned a gift to be done to another user; this info will be accessible on xmasg and also sent by mail.
User can subscribe, make a login and restore (through email) the password if lost.
Every house has got 2 dates:
- gift_date = when physically users will exchange their gift (no action on this platform)
- end_date = extraction date = when this platform will make a random extraction of the persone which every user would give a gift!
There are some operation that can be done on houses:
- private: not visible and accessible to not member;
- public: visible till end_date is expiring, and accessible to new members;
- dates can be changed (with logic);
- New member can be added or removed by admin;
- Admin can create or remove other member as admin;
- Every member can set some people as exclusions: he won't give a gift to that person (ex. to the girlfriend, you already are going to do a gift!)
The project is in italian for a simple reason: we'll use it next Christmas! 
The idea is to integrate this platform in the future with some functionality of different application, needed by me or my friends.


## File description
### RaspierreUnchained, templates, static
Contains settings, and base html and css, and a little bit of javascript used (or potentially used) by all applications.
The project is managed with docker!

### registration
Contains all files managing the resitration, login, logout, recover password, ...
There is no javascript

### xmasg
Contains the application for extraction of the gift!
in `*.py` files there are models, views, forms for interacting with DB, rendering pages and also some AJAX communication for js functions; in file `xmasg.py` there is the core code for randomly select giver and receiver. Template are divided in the 3 pages, and 2 element for organizing the sidebar. For static files, there is some CSS (but also bootstrap is used). and the core javscript is in `xmasg.js` file.

### Myself
it's a site for describing myself, done with django in order to modify content online


## Other

### Biblio
- Login template: https://codepen.io/colorlib/pen/rxddKy
- Login overwrite: https://learndjango.com/tutorials/django-password-reset-tutorial, 
https://stackoverflow.com/questions/53563534/template-password-reset-form-html-does-not-overwrite-the-django-admin-template
- SocketIO: https://channels.readthedocs.io/en/latest/tutorial/part_1.html
- CSRF: https://docs.djangoproject.com/en/3.0/ref/csrf/
- AJAX: https://zerowithdot.com/django-2-ajax-call/, http://musings.tinbrain.net/blog/2015/aug/28/vanilla-js-meets-djangos-csrf/
- Event scheduler: https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6, https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html
- https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/ USED FOR DEPLOY!!!!

### Note
Pay attention to date!
Data are store in DB as UTC=0, Italy is UTC=+1 (CET), but in winter is +2 (CEST) because of daylight