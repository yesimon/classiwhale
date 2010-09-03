#!/usr/bin/python2.7

# modify this later
# not setup now!

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

# dump the data to fixtures
os.system('python manage.py dumpdata tweed --indent=2 > tweed/models/fixtures/data.json')
# drop and recreate the db (this is for postgres)
os.system('dropdb authy')
os.system('createdb authy --encoding=UTF-8')
# sync the db
os.system('python manage.py syncdb --noinput')

# create a super user
from django.contrib.auth.models import User
u = User.objects.create(
        username='simon',
            first_name='',
            last_name='',
            email='sye737@gmail.com',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
u.set_password('wombocombo')
u.save()
print "User account created"

# load the fixtures back in
os.system('python manage.py loaddata data.json')
# run the server
os.system('python manage.py runserver')
