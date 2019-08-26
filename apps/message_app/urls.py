from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^messages/(?P<appointment_id>\d+)$', views.index),
]
