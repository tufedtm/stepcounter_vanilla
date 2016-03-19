from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'main.views.index', name='index'),

    url(r'^profile/(?P<user_id>[\d]+)$', 'main.views.profile', name='profile'),
    url(r'^profile/edit/(?P<user_id>[\d]+)$', 'main.views.profile_edit', name='profile_edit'),
    url(r'^profile/users$', 'main.views.profiles', name='users'),

    url(r'^profile/edit/access/(?P<user_id>[\d]+)$', 'main.views.profile_edit_form', name='profile_edit_form'),

    url(r'^login$', 'main.views.step_login', name='login'),
    url(r'^logout$', 'main.views.step_logout', name='logout')
]