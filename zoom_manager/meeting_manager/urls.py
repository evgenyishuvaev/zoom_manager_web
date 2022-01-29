from django.urls import path

from . import views


urlpatterns = [
    path('', views.meetings_page, name='meetings_page'),
    # path('api/refresh_token', views.refresh_zoom_token, name='refreshButton'),
    path('api/users', views.send_zoom_users_to_web_ui, name='getUsersButton'),
    path('api/all_meetings', views.send_all_zoom_meetings_to_web_ui, name='getAllMeetingsButton'),
]