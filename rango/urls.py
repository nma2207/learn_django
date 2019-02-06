from . import views

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name = 'add_category'),
    url(r'^(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.regicter, name='register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name = 'logout'),
    url(r'^search/$', views.search, name = 'search'),
    url(r'^goto/$', views.track_url, name = 'goto'),
    url(r'^profile/$', views.profile, name = 'profile')
]