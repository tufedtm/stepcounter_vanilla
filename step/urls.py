from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from main import views

urlpatterns = [
    url(r'^', include('main.urls')),

    url(r'^api/v1/', include('api.urls')),
    url(r'^api-step-test/', login_required(views.testy), name='testy'),

    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
