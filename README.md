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


## Program description
The project is solved with Django and Javascript.
The idea is to solve a real world problem: with my group of friends, for Christmas, we randomly select who is going to give a present to who --> everybody is going to receive a present from a random person; the idea is that 1 big gift is better than many little gift!
The project is a platform where user can subscribe, selecting to participate in a "house", and there they will be randomly assigned a gift to be done to another user.


### File description
