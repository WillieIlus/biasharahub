from django.contrib import admin

from .models import User, Network, SocialProfile

admin.site.register(User)
admin.site.register(Network)
admin.site.register(SocialProfile)
