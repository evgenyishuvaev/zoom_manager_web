from django.urls import path

from . import views


urlpatterns = [
    path('', views.meetings_page, name='meetings_page')
]