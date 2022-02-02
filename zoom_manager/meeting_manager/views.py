from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .services.ZoomAPI.zoom_api import refresh_token, get_users_list, get_meetings_from_all_users
from .models import ZoomUsers


@login_required
def meetings_page(request):
    return render(request, "meeting_manager/index.html")

@login_required
def send_zoom_users_to_web_ui(request):

    zoom_users = ZoomUsers.objects.all()
    result = {}

    for user in zoom_users:
        result[user.host_id] = user.email

    return JsonResponse(result)

@login_required
def send_all_zoom_meetings_to_web_ui(request):

    zoom_users_id = []
    zoom_users = ZoomUsers.objects.all()

    for user in zoom_users:
        zoom_users_id.append(user.host_id)

    result = {
        "result": get_meetings_from_all_users(zoom_users_id=zoom_users_id),
        "users": {},
        }

    for user in zoom_users:
        result["users"][user.host_id] = user.email
    
    return JsonResponse(result)