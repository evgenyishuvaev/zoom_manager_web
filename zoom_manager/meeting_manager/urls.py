from django.urls import path

from . import views


urlpatterns = [
    path('', views.meetings_page, name='meetings_page'),
    # path('api/refresh_token', views.refresh_zoom_token, name='refreshButton'),
    path('api/v1/users', views.send_zoom_users_to_web_ui, name='getUsersButton'),
    path('api/v1/users_zoom', views.get_users_from_zoom, name='getUsersFromZoomButton'),
    path('api/v1/all_meetings', views.send_all_zoom_meetings_to_web_ui, name='getAllMeetingsButton'),
    path('api/v1/create', views.create_zoom_meeting , name='createMeeting'),
]