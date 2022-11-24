from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib.parse
import requests

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def login(request):
    # getting ticket from request
    ticket = request.GET.get('ticket', None)
    # if ticket is not None, then we have to validate it
    if ticket != None:
        # creating service url
        params = urllib.parse.urlencode({'service' : request.build_absolute_uri(), 'ticket' : ticket})
        url = f"https://auth.mephi.ru/validate?{params}"
        payload={}
        headers = {}
        # sending request to CAS server
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            return HttpResponse("Error while validating user.")
        # if response is not empty, then we have to parse it
        resp = response.text.split()
        # structure of response if auth is ok:
        # yes
        # gvrybina

        # structure of response if auth is not ok:
        # no

        # if auth is ok, then we show login
        if 'yes' in resp:
            user_login = resp[1]
            return HttpResponse(f"User validated, login {user_login}")
        
        # if auth is not ok, then we show error
        return HttpResponse("User not validated.")
        
    # if ticket is None, then we have to redirect user to CAS server
    params = urllib.parse.urlencode({'service' : request.build_absolute_uri()})
    return redirect(f"https://auth.mephi.ru/login?{params}")
