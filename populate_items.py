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

def createImage(title):
    im = Image.new("RGB",(512,512),"rgb(237,237,240)")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('skirmisher.ttf',60)
    draw.text((100,200),title,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font)
    im.save('media/media/'+title+'.jpg')

def add_prod(tit, desc, prc, tim, img1,img2,img3,own):
    p = Product.objects.get_or_create(title=tit, description=desc, price=prc, time=tim, image1=img1, image2=img2, image3=img3,owner=own)[0]
    return p


def populate():
    user_list = UserProfile.objects.all()
    no_of_users = len(user_list)
    for i in range(1,21):
        title = 'product'+str(i)
        desc = 'This is '+title
        prc = 10*i+9
        tim=datetime.datetime.now()
        createImage(title)
        img1 = "media/"+title+".jpg"
        createImage(title+'b')
        img2 = "media/"+title+"b.jpg"
        createImage(title+'c')
        img3 = "media/"+title+"c.jpg"
        ran=random.randint(0,no_of_users-1)
        own = user_list[ran]
        

        add_prod(tit = title,
            desc = desc,
            prc=prc,
            tim=tim,
            img1=img1,
            img2=img2,
            img3=img3,
            own=own)

if __name__ == '__main__':
    print "Starting Listing population script..."
    populate()
    

    for p in Product.objects.all():
        print "- {0}".format(str(p))



