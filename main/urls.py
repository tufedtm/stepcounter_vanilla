from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^profile/(?P<user_id>[\d]+)$', views.profile, name='profile'),
    url(r'^profile/edit/(?P<user_id>[\d]+)$', views.profile_edit, name='profile_edit'),
    url(r'^profile/edit/access/(?P<user_id>[\d]+)$', views.profile_edit_form, name='profile_edit_form'),
    url(r'^profile/users$', views.profiles, name='users'),

    url(r'^login$', views.step_login, name='login'),
    url(r'^logout$', views.step_logout, name='logout')
]
