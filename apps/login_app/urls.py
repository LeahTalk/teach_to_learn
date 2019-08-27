from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^process_register$', views.register),
    url(r'^register$', views.continue_registration),
    url(r'^category_form$', views.select_category),
    url(r'^subcategory_form$', views.select_subcategory),
    url(r'^learn_subcategories$', views.choose_subcategories),
    url(r'^location_form$', views.location_form_process),
    url(r'^register_login$', views.register_login),
]
