from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib.parse
import requests

# Create your views here.

def index(request):
    # return HttpResponse("Hello, world. You're at the home_auth index.")
    return render(request, 'index.html', {})

def login(request):
    # redirect to login page at home.mephi.ru
    # validate user
    # if request.user.is_authenticated:
    #     return HttpResponse("You are already logged in.")
    
    ticket = request.GET.get('ticket', None)
    if ticket != None:
        params = urllib.parse.urlencode({'service' : request.build_absolute_uri(), 'ticket' : ticket})
        url = f"https://auth.mephi.ru/validate?{params}"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            return HttpResponse("Error while validating user.")
        resp = response.text.split()
        if 'yes' in resp:
            user_login = resp[1]
            return HttpResponse(f"User validated, login {user_login}")
            
        return HttpResponse("User not validated.")
    params = urllib.parse.urlencode({'service' : request.build_absolute_uri()})
    # print(curr_url)
    # return HttpResponse("Hello, world. You're at the home_auth login page. <a href='https://home.mephi.ru/cas/login?service=" + curr_url + "'>Login</a>")
    return redirect(f"https://auth.mephi.ru/login?{params}")
