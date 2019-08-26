from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^process_register$', views.register),
    url(r'^register$', views.complete_register),
    url(r'^register_login$', views.register_login)
]
