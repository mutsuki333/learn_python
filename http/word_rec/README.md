
# Using notes
### *Google API might stop Django from runing*
#### [ref](https://stackoverflow.com/questions/34758516/google-calendar-api-stops-django-from-starting)
### Replace
```python
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
```
### with
```python
flags = tools.argparser.parse_args([])
```
