"""step URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url


urlpatterns = [
    url(r'^login$', 'api.views.api_login', name='api_login'),
    url(r'^registration$', 'api.views.api_reg', name='api_reg'),
    url(r'^step_update$', 'api.views.step_update', name='step_update'),
    url(r'^step_info$', 'api.views.api_info', name='api_info'),
    url(r'^step_info_update$', 'api.views.api_info_update', name='api_info_update'),

    url(r'^history', 'api.views.history', name='history'),
]
