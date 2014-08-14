from django.conf.urls import patterns, url
from listing import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^product/(?P<product_name_url>\w+)/$', views.products_page, name='products_page'),
        url(r'^add_item/$',views.add_item,name='add_item'),
        url(r'^register/$',views.register,name='register'),
	url(r'^login/$', views.user_login,name='login'),
	url(r'^logout/$',views.user_logout,name='logout'),
        url(r'^product/(?P<product_id>\w+)/shortlist$', views.shortlist_item, name='shortlist'),
        url(r'^product/(?P<product_id>\w+)/place_order$', views.place_order, name='place_order'),
        url(r'^notification/$', views.display_notification,name='display_notification'),
        url(r'^(?P<id>\w+)/mod_item/$',views.mod_prod,name='mod_item'),
        )