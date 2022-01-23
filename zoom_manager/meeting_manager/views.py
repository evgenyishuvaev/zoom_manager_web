from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def meetings_page(request):
    return render(request, "meeting_manager/index.html")