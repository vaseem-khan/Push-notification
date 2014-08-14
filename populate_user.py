import os
import sys
import datetime
import random
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifsys.settings')
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
from listing.models import Product, Notification, UserProfile
from django.contrib.auth.models import User

def add_user(username):
	email = '{0}@{0}.{0}'.format(username)
	u=User.objects.create_user(username=username,email=email)
	u.set_password('1234')
	u.save()
	UserProfile.objects.create(user=u)

if __name__=='__main__':
	for i in range(10):
		name = 'user'+str(i)
		add_user(name)
