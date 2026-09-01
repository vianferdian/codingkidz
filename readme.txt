email = superadmin@example.com
email = admin@example.com
password = asdf@1234

Step1) Go To settings.py put your EMAIL_HOST_USER here

------> EMAIL_HOST_USER=''

Step2) Go To .env file and put your EMAIL_HOST_PASSWORD here

------> EMAIL_HOST_PASSWORD=''

Step3) Create virtual environment

------>python -m venv env
------>cd env
------>env$cd Script
------\env\Script>activate
------\env\Script>cd ..
------\env>cd ..
------\dashboard>

Step4) Install the django template requirements

------\dashboard>pip install -r requirements.txt

Step5) apply migrations and migrate

------\dashboard>python manage.py makemigrations
------\dashboard>python manage.py migrate
------\dashboard>python manage.py createsuperuser

or

You can change the existing superuser password using:

------\dashboard>python manage.py changepassword superadmin@example.com


Step6) Know you can run your template using:

------\dashboard>python manage.py runserver

or 

if you want to access your project in network type:

------\dashboard>python manage.py runserver 0.0.0.0:8000

check your ip using 'ipconfig' in command prompt

if you ip is 192.168.1.1

than network url is 192.168.1.1:8000
