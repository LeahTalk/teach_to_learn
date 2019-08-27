from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^appointment$', views.index),
    url(r'^appointment/add$', views.process_new_appointment),
    url(r'^appointment/edit/(?P<appointment_id>\d+)$', views.edit_appointment),
    url(r'^appointment/reserve/(?P<appointment_id>\d+)$', views.reserve_appointment),
    url(r'^appointment/cancel/(?P<appointment_id>\d+)$', views.cancel_appointment),
    url(r'^process_reservation$', views.process_reservation),
]
