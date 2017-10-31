from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<user_name>.*)/', views.create_letter, name='create_letter'),
]
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )