from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .services.ZoomAPI.zoom_api import refresh_token, get_users_list, get_meetings_from_all_users
from .models import ZoomUsers


# Create your views here.
def meetings_page(request):
    return render(request, "meeting_manager/index.html")

# def refresh_zoom_token(request):
#     result = {"result" : refresh_token()}
#     return JsonResponse(result)

def send_zoom_users_to_web_ui(request):
    # result = {"result" : get_users_list()}
    
    zoom_users = ZoomUsers.objects.all()
    result = {}

    for user in zoom_users:
        result[user.host_id] = user.email

    return JsonResponse(result)

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