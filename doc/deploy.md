 Setting up the Development Environment
----

#### Cloning the project

```git clone https://github.com/mfgmateus/bookfree.git```


```cd bookfree```

#### Creating the Virtual Environment
 
Using ```virtualenv``` we'll create a virtual environment.

```virtualenv flask```

#### Installing the Flask Modules
 
In this project, it's required to install the following modules:

```flask/bin/pip install Flask```

```flask/bin/pip install flask-login```

```flask/bin/pip install flask-mail```

```flask/bin/pip install flask-sqlalchemy```

```flask/bin/pip install flask-migrate```

```flask/bin/pip install flask-wtf```

#### Activate Flask and Running the application

Type the following command to enter inside the virtualenv:

```source flask/bin/activate```

Finally to start the application...

```python run.py runserver```

To leave the virtualenv just type ```deactivate```.
