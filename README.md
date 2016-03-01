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

You're good to go!
