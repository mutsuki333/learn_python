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


## Simple server can be used with  
`python -m http.server`
