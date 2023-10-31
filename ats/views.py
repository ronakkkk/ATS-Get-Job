import datetime
import json
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from ats.models import CustomUser
from django.conf import settings
from .models import Upload
import boto3

# Connect to S3 
# s3 = boto3.client(
#    "s3",
#    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
# )

@csrf_exempt
def get_s3_file(request):
    email = request.COOKIES.get('email')
    user = CustomUser.objects.get(email=email)
    filename = str(user.id)+".pdf"

    # Construct the S3 key (object key) based on the filename
    s3_key = 'resumes/'+filename  # You may need to prepend a folder or path if you've used one
    url = 'https://'+settings.AWS_S3_CUSTOM_DOMAIN+'/'+s3_key
    try:
        response = requests.head(url)
        # Check if the status code is in the 2xx range, which indicates a valid URL
        if 200 <= response.status_code < 300:
            return JsonResponse({'Link': url})
        else:
            return JsonResponse({'error': "Resume Not Found"})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
def upload_to_s3(request):
    if request.method == 'POST':

        file = request.FILES['resume']
        # Get file info
        email = request.COOKIES.get('email')
        user = CustomUser.objects.get(email=email)
        file.name = str(user.id)+".pdf"
        print(file.name)
        print(email)
        # Build unique key using email 
        # key = f'{email}/resume.pdf'
        upload = Upload(file=file)
        upload.save()   
        resume_url = upload.file.url
        return JsonResponse({'resumeUrl': resume_url, 'message': 'Success'})

# from django.contrib.auth.models import User
# from .models import User

@login_required
@csrf_exempt
def upload_resume(request):
    return render(request, "upload_resume.html")

def index(request):
    return render(request, "index.html")
@csrf_exempt
def signUpUser(request):
    return render(request, "signup.html")
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        # data = json.loads(request.body.decode('utf-8'))

        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        print(email)
        print(full_name)
        print(password)
        if not (email and full_name and password):
            return JsonResponse({'error': 'Missing required data'}, status=400)

        user = CustomUser.objects.create_user(email=email, full_name=full_name, password=password)
        user.save()
        return render(request, "upload_resume.html")

def checkUserDetails(request):
    emailID = request.POST.get("email_id")
    password = request.POST.get("password")
    print(emailID, password)
    user = authenticate(request, email=emailID, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        # Login the user
        login(request, user) 
        response = redirect('upload_resume')
        # Set tokens as cookies
        response.set_cookie('refresh', str(refresh)) 
        response.set_cookie('access', str(access))
        response.set_cookie('email', emailID)
        return response
        # return redirect(request, "upload_resume.html")
    else:
            return render(request, "index.html", {
            "message": "Invalid username and/or password."
        })
    # if emailID == "r@g.com" and password == "123":        
    #     print("Matched")
    #     return render(request, "upload_resume.html")
    # else:
    #     return render(request, "index.html", {
    #         "message": "Invalid username and/or password."
    #     })
    