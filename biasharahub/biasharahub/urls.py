"""biasharahub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.contrib.sitemaps.views import index, sitemap
from django.urls import path, include

from biasharahub.views import Home, NewsletterView
from business.sitemaps import BusinessSitemap
from reviews.sitemaps import ReviewSitemap

sitemaps = {
    'business': BusinessSitemap,
    'review': ReviewSitemap,

}
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', Home.as_view(), name='home'),
                  path('newsletter', NewsletterView.as_view(), name='newsletter'),
                  path('accounts/', include('allauth.urls', )),
                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  path('categories/', include('categories.urls', namespace='categories')),
                  path('business/', include('business.urls', namespace='business')),
                  path('reviews/', include('reviews.urls', namespace='reviews')),
                  path('comments/', include('comments.urls', namespace='comments')),
                  path('invitations/', include('invitations.urls', namespace='invitations')),
                  path('locations/', include('locations.urls', namespace='locations')),
                  path('opening-hours/', include('openinghours.urls', namespace='openinghours')),
                  path('about-us/', flatpage, {'url': '/about-us/'}, name='about'),
                  path('contact-us/', flatpage, {'url': '/contact-us/'}, name='contact'),
                  path('policy/', flatpage, {'url': '/policy/'}, name='policy'),

                  path('sitemap.xml', index, {'sitemaps': sitemaps}),
                  path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
