from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^messages/(?P<appointment_id>\d+)$', views.index),
    url(r'^send_message/(?P<appointment_id>\d+)$', views.send_message),
]
