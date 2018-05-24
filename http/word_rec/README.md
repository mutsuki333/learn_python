# Django notes
### **Run test server**
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
### **Django templates syntax** \: [ref](https://docs.djangoproject.com/en/1.7/topics/templates/)
**Variables** look like : **``{{ variables }}``**

**Filters** look like : **``{{ variables|Filters }}``**
> ``{{ variables|lower }}`` to convert text to lowercase.
> 


### **File path in Django project** \: [ref](https://stackoverflow.com/questions/17406126/how-can-i-use-relative-path-to-read-local-files-in-django-app)
Use `absolute path` can be a easier way. Declare something like `FILES_FOLDER` in the settings.py.
```Python
import os
FILES_FOLDER = os.path.join(BASE_DIR, 'relative_path/')
```
and `from yourproject.settings import FILES_FOLDER`, or just simply import `BASE_DIR` on the run.
```Python
import os
from yourproject.settings import BASE_DIR
file_path = os.path.join(BASE_DIR, 'relative_path')
```
Bear in mind that the relative path is from your Django pro


### **A good structure example** \: [ref](https://stackoverflow.com/questions/22841764/best-practice-for-django-project-working-directory-structure)
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


# Google API
### **Google APIs python install** \: [ref](https://developers.google.com/drive/api/v3/quickstart/python)
#### requirements
* Python 2.6 or greater.
* The pip package management tool.
* A Google account with Google Drive enabled.
#### install
```shell
pip install --upgrade google-api-python-client
```

### **Google API might stop Django from runing** \: [ref](https://stackoverflow.com/questions/34758516/google-calendar-api-stops-django-from-starting)
Replace
```python
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
```
with
```python
flags = tools.argparser.parse_args([])
```
