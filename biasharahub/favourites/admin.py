from django.contrib import admin

from .models import Bookmark, Vote

admin.site.register(Bookmark)
admin.site.register(Vote)