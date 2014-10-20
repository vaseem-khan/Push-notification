from celery import task
import json
import redis
import datetime
from django.utils import timezone
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from listing.models import Product,Notification,UserProfile
from listing.forms import ProductForm, UserForm
from django.dispatch import receiver

@task
def create_notification_subscribe(product, current_user):
    actingUser = current_user.user.username
    for each in product.subscribers.all():
        if each.user.username!=actingUser:
            n=Notification.objects.create(title="subscribed by %s" % actingUser,message="{0} has also shortlisted this listing {1}".format(actingUser,product.title),acting_user=actingUser,time=timezone.now())
            each.Notifications.add(n)
            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
            for session in each.user.session_set.all():
                redis_client.publish(
                    'notifications.%s' % session.session_key,
                    json.dumps(
                        dict(
                            # time = n.time,
                            message=n.message,
                            recipient=each.user.username
                            )
                        )
                    )
@task
def create_notification_place(product, current_user):
    actingUser = current_user.user.username
    n=Notification.objects.create(title="offer placed by %s" % actingUser,message="{0} has placed an offer on {1}".format(actingUser,product.title),acting_user=actingUser,time=timezone.now())
    product.owner.Notifications.add(n)
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    for session in product.owner.user.session_set.all():
        redis_client.publish(
            'notifications.%s' % session.session_key,
            json.dumps(
                dict(
                    # time = n.time,
                    message=n.message,
                    recipient=product.owner.user.username
                    )
                )
            )

    for each in product.placed_users.all():
        if each.user.username!=actingUser:
            n=Notification.objects.create(title="placed by %s" % actingUser,message="{1} has recieved a new offer by {0}".format(actingUser,product.title),acting_user=actingUser,time=timezone.now())
            each.Notifications.add(n)
            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
            for session in each.user.session_set.all():
                redis_client.publish(
                    'notifications.%s' % session.session_key,
                    json.dumps(
                        dict(
                            # time = n.time,
                            message=n.message,
                            recipient=each.user.username
                            )
                        )
                    )

    for each in product.subscribers.all():
        if each.user.username!=actingUser:    
            n=Notification.objects.create(title="placed by %s" % actingUser,message="{1} has recieved a new offer by {0}".format(actingUser,product.title),acting_user=actingUser,time=timezone.now())
            each.Notifications.add(n)
            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
            for session in each.user.session_set.all():
                redis_client.publish(
                    'notifications.%s' % session.session_key,
                    json.dumps(
                        dict(
                            # time = n.time,
                            message=n.message,
                            recipient=each.user.username
                            )
                        )
                    )


