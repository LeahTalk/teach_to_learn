from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^dashboard$', views.index),
    url(r'^profile/(?P<user_id>\d+)$', views.view_profile),
    url(r'^my_history$', views.view_history),
    url(r'^categories$', views.categories),
]
