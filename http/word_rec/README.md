# Django notes
### **A good structure example** \:[ref](https://stackoverflow.com/questions/22841764/best-practice-for-django-project-working-directory-structure)
```
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
```cmd
pip install --upgrade google-api-python-client
```

### **Google API might stop Django from runing** \: [ref](https://stackoverflow.com/questions/34758516/google-calendar-api-stops-django-from-starting)
#### Replace
```python
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
```
#### with
```python
flags = tools.argparser.parse_args([])
```
