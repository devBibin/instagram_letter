from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^(?P<user_name>.*)/', views.create_letter, name='create_letter'),
]