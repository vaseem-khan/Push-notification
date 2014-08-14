from django.contrib import admin
from listing.models import Product, Notification, UserProfile

admin.site.register(Product)
admin.site.register(Notification)
admin.site.register(UserProfile)
