from django.shortcuts import render

# Create your views here.
import asyncio
from django.http import HttpResponse
from django.views import View


def index(request):
    # await asyncio.sleep(1)





    return HttpResponse("Hello, world. You're at the polls index.")