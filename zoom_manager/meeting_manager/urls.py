from django.urls import path

from . import views


urlpatterns = [
    path('', views.meetings_page, name='meetings_page'),
    path('api/refresh_token', views.refresh_zoom_token, name='refreshButton')
]