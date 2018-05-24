
# Using notes
#### *Google APIs python install*
##### [ref](https://developers.google.com/drive/api/v3/quickstart/python)
#### requirements
* Python 2.6 or greater.
* The pip package management tool.
* A Google account with Google Drive enabled.
#### install
```cmd
pip install --upgrade google-api-python-client
```

#### *Google API might stop Django from runing*
##### [ref](https://stackoverflow.com/questions/34758516/google-calendar-api-stops-django-from-starting)
#### Replace
```python
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
```
#### with
```python
flags = tools.argparser.parse_args([])
```
