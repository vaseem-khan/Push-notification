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
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import task

def index(request):
    context=RequestContext(request)
    product_list=Product.objects.order_by('-time')

    context_dict={'products':product_list}
    for product in product_list:
        product.url = product.id
    return render_to_response('listing/index.html',context_dict,context)

def products_page(request,product_name_url):
    context = RequestContext(request)
    context_dict={}

    try:
        product=Product.objects.get(id=product_name_url)
        
        context_dict={'product':product}
    except Product.DoesNotExist:
        return HttpResponseNotFound('<h1>404 you are lost No Page Here</h1>')

    if request.user.is_authenticated():
        is_owner, has_shortlisted, has_placed = False,False,False
        if product.owner==request.user.userprofile:
            is_owner=True
        else:
            if request.user.userprofile in product.subscribers.all():
                has_shortlisted = True
            if request.user.userprofile in product.placed_users.all():
                has_placed = True
        context_dict['is_owner']=is_owner
        context_dict['has_placed']=has_placed
        context_dict['has_shortlisted']=has_shortlisted
    return render_to_response('listing/product.html',context_dict,context)

@login_required
def shortlist_item(request,product_id):
    context = RequestContext(request)
    current_user = request.user.userprofile
    product=Product.objects.get(id=product_id)
    task.create_notification_subscribe.delay(product,current_user)
    product.subscribers.add(current_user)
    return HttpResponseRedirect('/listing/product/'+str(product_id))

@login_required
def place_order(request,product_id):
    context = RequestContext(request)
    current_user = request.user.userprofile
    product=Product.objects.get(id=product_id)
    task.create_notification_place.delay(product,current_user)
    product.placed_users.add(current_user)

    return HttpResponseRedirect('/listing/product/'+str(product_id))



def register(request):
    context=RequestContext(request)

    registered = False

    if request.method=='POST':
        user_form = UserForm(data=request.POST)
        
        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            UserProfile.objects.create(user=user)

            registered = True
        else:
            print user_form.errors

    else:
        user_form = UserForm()

    return render_to_response('listing/register.html',{'user_form':user_form,'registered':registered},context)


def user_login(request):
    context = RequestContext(request)

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/listing/')
            else:
                return HttpResponse("Account is disabled")
        else:
            print "Invalid login details: {0}.{1}".format(username,password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('listing/login.html',{},context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/listing/')

@login_required
def add_item(request):
    context=RequestContext(request)
    added = False
    print request.method

    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.userprofile
            product.time=timezone.now()
            product.image1 = request.FILES['image1']
            if 'image2' in request.FILES:
                product.image2 = request.FILES['image2']
            if 'image3' in request.FILES:
                product.image3 = request.FILES['image3']
            product.save()
            added = True
        else:
            print form.errors

    else:
        form = ProductForm()

    return render_to_response('listing/add_item.html',{'form':form,'added':added},context)


@login_required
def mod_prod(request, id):
    context=RequestContext(request)
    product = Product.objects.get(id=id)
    mod = False

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():

            product = form.save(commit=False)
            if 'image1' in request.FILES:
                product.image1 = request.FILES['image1']
            if 'image2' in request.FILES:
                product.image2 = request.FILES['image2']
            if 'image3' in request.FILES:
                product.image3 = request.FILES['image3']
            product.time=timezone.now()
            product.save()
            mod = True
        else:
            print form.errors
    else:
        form = ProductForm(instance=product)

    return render_to_response('listing/mod_item.html',{'form':form, 'mod':mod, 'id':id},context_instance=RequestContext(request))


@login_required
def display_notification(request):
    context=RequestContext(request)
    current_user = request.user.userprofile
    viewed = current_user.Notifications.filter(viewed=True).order_by('-time')
    unread = current_user.Notifications.filter(viewed=False).order_by('-time')
    l=len(unread)
    context_dict={'unread':unread,'viewed':viewed,'l':l}
    response = render_to_response('listing/notification.html',context_dict,context)
    for notif in unread:
        notif.viewed = True
        notif.save()
    return response