
# A Simple Blog Project

## This project is made using Django framework in Python

***

## Requirements

+ **Python 3.8.x**
+ **Pip 21.2.x**

## Notes

> In Windows use ```python``` in the command line. Windows CMD recognizes **Python3** using ```python```

> In linux use ```python3``` instead as using ```python``` is recognized as **Python2.x** version.

## Steps

+ Create a directory (eg: blogApp) <br>```cd blogApp```
+ Clone the repository <br>```git clone https://github.com/pravesh-k/simple-blog-django.git```
+ Check pip exists or not<br>```pip -h```
+ Install virtualenv<br>```pip install virtualenv```
+ Create a virtual env<br>```virtualenv my_env``` OR ```python -m venv my_env```
+ Activate the virtual env,
  + For windows: ```my_env\Scripts\activate```
  + For linux:  ```source my_env/bin/activate```
+ Install django framework<br>```pip install "Django==3.0.*"```
+ Change directory<br>```cd simple-blog-django/```
+ Run the application<br>```python manage.py runserver```
+ In a browser hit the url<br>http://localhost:8000/blog/
+ Done! End!
