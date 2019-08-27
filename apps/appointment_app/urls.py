from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^appointment$', views.index),
    url(r'^add_appointment$', views.process_new_appointment),
    url(r'^edit_appointment/(?P<appointment_id>\d+)$', views.edit_appointment),
    url(r'^reserve_appointment/(?P<appointment_id>\d+)$', views.reserve_appointment),
    url(r'^process_reservation$', views.process_reservation),
]
