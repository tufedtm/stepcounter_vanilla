from django.conf.urls import url
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^login/$', views.api_login, name='login'),
    url(r'^registration/$', views.api_reg, name='registration'),

    url(r'^get_info/$', views.api_info, name='get_info'),

    url(r'^step_update/$', views.step_update, name='step_update'),

    url(r'^step_info_update/$', views.api_info_update, name='api_info_update'),

    url(r'^history/$', views.history, name='history'),
]
