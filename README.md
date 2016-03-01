# plog
Plivo Assignment - Blog : "Plog"

Install the following packages

pip3 install django
pip3 install djangorestframework

Clone this repository in the var/www/html folder and update your site.conf file to reflect the path.

Assuming you have apache mod_wsgi and my sql installed and enabled, follow this documentation to deploy using mod_wsgi : https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/

run,
sudo a2ensite site.conf
sudo service apache2 reload

Create a settings.py file in the plog root folder. Update the database name and password and specify mysql database engine is being used.
Make sure mysql is installed and python mysqlclient library.
Create an empty database with the name you gave in the settings.py file.

From the site root, run:
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsupersuser
Note: Fill in the prompted fields

Collectstatic will collect all your static files and consolidate it into a single folder.
Beforing running collectstatic, make sure you have set the STATIC_ROOT directive in settings.py to the folder where you want to consolidate the static files.

You're good to go!
