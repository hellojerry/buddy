# buddy

This is the public-facing code for my "Accountabillibuddy" project, hosted at http://mjperrigue.com.

# About

This project is an app to avoid procrastination! You log in, give the app some times, and then the app calls you
and tells you to get to work if you miss your checkins! I built this on the theory that sometimes its easier to
get things done by avoiding other things.

# Notes

To get this installed, you'll want a python3 virtual environment, and you'll definitely want to do
do "pip3 install -r requirements.txt" at the command line. After getting the python packages
installed, you'll want to change into the static/app directory and do npm install and bower install to get the 
assorted javascript dependencies loaded. 

The "sample_keys.py" file under the buddy directory should be renamed to "keys.py" and need their values replaced
with your own info. 

This project runs with the following stack at deployment:

- Django
- Django REST Framework
- Angular JS
- Redis as a broker for Celery
- PostgreSQL
- Gunicorn and NGINX to run the server.

To get the project fully running on an EC2 instance, you'll want to get a Postgres RDS instance up and running
along with an Elasticache Redis instance, and then make sure their related ports are open on the EC2 instance.

To get this running locally, you'll want two command lines running, and you can probably afford to comment out
the Postgres info and replace it with the lighter weight sqlite database. A good guide to get celery running
with Redis locally can be found <a href='http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/'>here.</a>

On top of that, you'll want to run over to the celery documentation and get celery and celerybeat running as a daemon.
This is not to mention the various API keys you'll need from Twitter and Twilio. 
