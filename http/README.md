# Python server setup notes
## Simple server can be used with  
`python -m http.server`
## Python requirements 
pip freeze will list all python packages and its versions.  
```pip freeze > requirements.txt```  
To install the required packages  
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
`-n APP_NAME, --name=APP_NAME`|Adjust the name of Gunicorn process.(pip install setproctitle)






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
