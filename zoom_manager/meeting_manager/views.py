from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .services.ZoomAPI.zoom_api import refresh_token

# Create your views here.
def meetings_page(request):
    return render(request, "meeting_manager/index.html")

def refresh_zoom_token(request):
    result = {"result" : refresh_token()}
    return JsonResponse(result)
