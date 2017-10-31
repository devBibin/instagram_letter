from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<user_name>.*)/', views.create_letter, name='create_letter'),
]