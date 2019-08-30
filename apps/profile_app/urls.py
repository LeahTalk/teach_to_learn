from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^dashboard$', views.index),
    url(r'^profile/(?P<user_id>\d+)$', views.view_profile),
    #url(r'^my_history$', views.view_history),
    url(r'^categories$', views.categories),
    url(r'^edit_profile$', views.edit_profile),
    url(r'^process_profile_edits$', views.process_profile_edits),
    url(r'^edit_password$', views.process_password_edits),
    url(r'^edit_description$', views.process_description_edits),
    url(r'^populate_subcategories_display$', views.populate_subcategories_display),
    url(r'^check_picture$', views.upload_photo),
    url(r'^add_skill$', views.add_skill),
]
