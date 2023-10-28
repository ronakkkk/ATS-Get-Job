from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, "index.html")

def checkUserDetails(request):
    emailID = request.POST.get("email_id")
    password = request.POST.get("password")
    print(emailID, password)
    if emailID == "r@g.com" and password == "123":
        return render(request, "upload_resume.html")

    else:
        return render(request, "index.html", {
            "message": "Invalid username and/or password."
        })