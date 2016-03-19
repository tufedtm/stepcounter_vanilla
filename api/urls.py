from django.conf.urls import url
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^login/$', views.api_login, name='login'),
    url(r'^registration/$', views.api_reg, name='registration'),

    url(r'^get_info/$', views.api_info, name='get_info'),
    url(r'^update_info/$', views.api_info_update, name='update_info'),
    url(r'^update_steps/$', views.api_steps_update, name='update_steps'),
    url(r'^get_history/$', views.api_history, name='get_history'),
]
