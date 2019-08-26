from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^users/(?P<user_id>\d+)$', views.user_page)
]
