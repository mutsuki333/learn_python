# Python server setup notes
[ref](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/)
## Simple server can be used with  
`python -m http.server`
## Python requirements 
`pip freeze` will list all python packages and its versions.  
```pip freeze > requirements.txt```  
To **install** the required packages  
```pip install -r requirements.txt```  
    or  
```pip -r requirements.txt```  to run in the desired enviroment.

## Virtual enviroment
virtualenv|cmd
:---|---
install|`[sudo] pip install virtualenv`
setup|`virtualenv ENV`
access to the global site-packages|with flag `--system-site-packages`
start|`source bin/activate`
stop|`deactivate`

## Gunicorn
A Python WSGI HTTP Server for UNIX.  
**Install** : `pip install gunicorn`  
**Start** : `gunicorn APPNAME.wsgi` 

Commonly Used Arguments||
---|---
`-b BIND, --bind=BIND`|Specify a server socket to bind. <br> To specify an IP : HOST:PORT
`-w WORKERS, --workers=WORKERS`|The number of worker processes.
`-n APP_NAME, --name=APP_NAME`|Adjust the name of Gunicorn process. (pip install setproctitle)
`-u USER, --user USER`|Switch worker processes to run as this user.
`-g GROUP, --group GROUP`|Switch worker process to run as this group.

## Editting a bash script to start Gunicorn
```bash
#!/bin/bash

NAME="word_rec"                                  # Name of the application
DJANGODIR=/home/mutsuki/code/learn_python/http/word_rec             # Django project directory
SOCKFILE=/home/mutsuki/code/learn_python/http/word_rec/run/gunicorn.sock  # we will communicte using this unix socket
USER=mutsuki                                     # the user to run as
GROUP=webapp                                     # the group to run as
NUM_WORKERS=3                                    # how many worker processes should Gunicorn spawn
#NUM_WORKERS=1
DJANGO_SETTINGS_MODULE=word_rec.settings         # which settings file should Django use
DJANGO_WSGI_MODULE=word_rec.wsgi                 # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ENV/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ENV/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --log-file=-
  #--bind=0.0.0.0:3000 \
```
Change the script fill to executable.  
`sudo chmod u+x gunicorn_start`

## Starting and monitoring with Supervisor
**install** : `sudo apt-get install supervisor`
When Supervisor is installed you can give it programs to start and watch by creating configuration files in the `/etc/supervisor/conf.d` directory.  
[ref.](http://supervisord.org/configuration.html#program-x-section-example)  
in `/etc/supervisor/conf.d/word_rec.conf`
```conf
[program:word_rec]
command = /home/mutsuki/word_rec/gunicorn_start                       ; Command to start app
user = mutsuki                                                        ; User to run as
stdout_logfile = /home/mutsuki/word_rec/logs/gunicorn_supervisor.log  ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                       ; Set UTF-8 as default encoding]
```
Create the file to store your application’s log messages:
```shell
mkdir /word_rec/logs/
touch word_rec/logs/gunicorn_supervisor.log 
```
**To start**
```shell
$ sudo supervisorctl reread
word_rec: available
$ sudo supervisorctl update
word_rec: added process group
```
Other commands `sudo supervisorctl COMMAND APPNAME`.  
`status`, `stop`, `start`, `restart`

## Nginx
**install** : `sudo apt-get install nginx`  
**start** : `sudo systemctl start nginx`  
**Other commands** : `status`, `stop`, `start`, `restart`.

Each Nginx virtual server should be described by a file in the *`/etc/nginx/sites-available directory`*. You select which sites you want to enable by making **symbolic links** to those in the *`/etc/nginx/sites-enabled`* directory.  
In `/etc/nginx/sites-available/word_rec`  
```Nginx
upstream hello_app_server {

      # fail_timeout=0 means we always retry an upstream even if it failed
      # to return a good HTTP response (in case the Unicorn master nukes a
                # single worker for timing out).

      server unix:/home/mutsuki/word_rec/run/gunicorn.sock fail_timeout=0;
}

server {

    listen   80;

    client_max_body_size 4G;

    access_log /home/mutsuki/word_rec/logs/nginx-access.log;
    error_log /home/mutsuki/word_rec/logs/nginx-error.log;

    location /static/ {
        alias   /home/mutsuki/word_rec/static/;
    }

    location /media/ {
        alias   /home/mutsuki/word_rec/image;
    }

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
          #if (!-f $request_filename) {
          #    proxy_pass http://hello_app_server;
          #    break;
          #}
              
        # Error pages
        error_page 500 502 503 504 /500.html;
        location = /500.html {
            root /webapps/hello_django/static/;
    }
    
}
```
Then  
```
sudo ln -s /etc/nginx/sites-available/word_rec /etc/nginx/sites-enabled/word_rec
```
    $ sudo service nginx restart


# Django notes
## **Run test server**
```shell
python manage.py runserver
```
Specify which port to listen on by giving the port as a parameter.
```shell
python manage.py runserver 3000
```
Listen to global by
```shell
python manage.py runserver 0.0.0.0:3000 #or 0:3000 for short.
```
## **Django templates syntax** \: [ref](https://docs.djangoproject.com/en/1.7/topics/templates/)
### **Variables** look like : `{{ variables }}`

### **Filters** look like : `{{ variables|Filters }}` : [more](https://docs.djangoproject.com/en/1.7/ref/templates/builtins/#ref-templates-builtins-filters)
> `{{ variables|lower }}` to convert text to lowercase.
> `{{ list|join:", " }}` to join a list with commas and space.
> `{{ value|default:"nothing" }}` If **value** isn’t provided or is empty, the above will display “**nothing**”.


### **for**
```django
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

### **if**, **elif**, and **else**
```django
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```
```django
{% if athlete_list|length > 1 %}
   Team: {% for athlete in athlete_list %} ... {% endfor %}
{% else %}
   Athlete: {{ athlete_list.0.name }}
{% endif %}
```

### **comment**
```django
{# greeting #}
```

### **Template inheritance**
```django
<!DOCTYPE html> {# base.html #}
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```
block tag tell the template engine that a child template may override those portions of the template.
```django
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

### **Turn off automatic HTML escaping**
```django
{# For individual variables #}
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}

{# For template blocks #}
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```


## **File path in Django project** \: [ref](https://stackoverflow.com/questions/17406126/how-can-i-use-relative-path-to-read-local-files-in-django-app)
Use `absolute path` can be a easier way. Declare something like `FILES_FOLDER` in the settings.py and `from yourproject.settings import FILES_FOLDER`
```Python
#settings.py
import os
FILES_FOLDER = os.path.join(BASE_DIR, 'relative_path/')
```
Or just simply import `BASE_DIR` on the run.
```Python
#some module
import os
from yourproject.settings import BASE_DIR
file_path = os.path.join(BASE_DIR, 'relative_path')
```
Bear in mind that the relative path is from your Django pro


## **A good Django structure example** \: [ref](https://stackoverflow.com/questions/22841764/best-practice-for-django-project-working-directory-structure)
```shell
~/projects/project_name/

docs/               # documentation
scripts/
  manage.py         # installed to PATH via setup.py
project_name/       # project dir (the one which django-admin.py creates)
  apps/             # project-specific applications
    accounts/       # most frequent app, with custom user model
    __init__.py
    ...
  settings/         # settings for different environments, see below
    __init__.py
    production.py
    development.py
    ...

  __init__.py       # contains project version
  urls.py
  wsgi.py
static/             # site-specific static files
templates/          # site-specific templates
tests/              # site-specific tests (mostly in-browser ones)
tmp/                # excluded from git
setup.py
requirements.txt
requirements_dev.txt
pytest.ini
...
```
