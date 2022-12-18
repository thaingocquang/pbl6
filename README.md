# Init project
cd to music/
1. `mkdir songs-stored`
2. `mkdir trains-database`


# Run project in localhost:
- turn on virtualenv
- install requirements `pip install -r requirements.txt`
- cd into ~/music
1. `python manage.py collectstatic`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py runserver`


# In production:

### Configure Nginx Web Server

- `sudo apt-get install nginx`
- create file: /etc/nginx/sites-available/`project-name`.conf
- create file: uwsgi_params
- sudo ln -s /etc/nginx/sites-available/`project-name`.conf /etc/nginx/sites-enabled/
- `python manage.py collectstatic`
- systemctl restart nginx
- 
===========
- docker run --name pbl6-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=music -itd mysql
- clone
- create venv
- install requirements.txt
- python manage.py collectstatic
- uwsgi --ini music_uwsgi.ini