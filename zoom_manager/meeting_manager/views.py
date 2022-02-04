from attr import asdict
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from .services.zoomapi.api import refresh_token, get_users_list, get_meetings_from_all_users
from .models import ZoomUsers
from .forms import CreateMeetingForms

@login_required
def meetings_page(request):
    return render(request, "meeting_manager/index.html")


def get_users_from_zoom(request):
    
    result = { "result" : get_users_list()} 
    return JsonResponse(result)


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

def get_data_for_create_meeting(request: HttpRequest):
    
    if request.method == "POST":
        form = CreateMeetingForms(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect("/meeting_manager")
    
    else:
        form = CreateMeetingForms()
        return render(request, "meeting_creating_forms.html", context={"form": form})