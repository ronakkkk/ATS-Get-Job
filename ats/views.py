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
import pandas
from ats.models import CustomUser
from django.conf import settings
from .models import Upload
import boto3
from . import resume_parse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


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
        # return JsonResponse({'resumeUrl': resume_url, 'message': 'Success'})
        return getJobs(request, resume_url)

def calculate_cosine_similarity(train_df, resume_text):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(train_df["description"])

    resume_tfidf_vector = tfidf_vectorizer.transform([resume_text])

    cosine_similarities = linear_kernel(resume_tfidf_vector, tfidf_matrix).flatten()
    train_df["cosine_similarity"] = cosine_similarities
    return train_df.nlargest(10, "cosine_similarity")

@csrf_exempt
def extract_resume(resume_url):
    skills, resume_txt = resume_parse.resume_screening(resume_url)
    s = ""
    for i in skills:
        s += i+", "

    return s[:-2], resume_txt

@csrf_exempt
def getJobs(request, resume_url):
    # parse resume
    skills, resume_txt = extract_resume(resume_url)
    # print(skills)
    country = 'us'
    per_page = '50'
    title = 'IT'
    full_time = 1 # 1 for yes 
    #part_time = 1 # 1 for yes
    # skills = 'python, java, C++, SQL, HTML, CSS, AWS, django'
    last_posted = '30' #last 7 days job posted
    APP_ID = '04e67ef5'
    API_KEY = '3c6fede16b773e46bf1aff00f481cbb5'
    BASE_URL = f'https://api.adzuna.com/v1/api/jobs/{country}'
    BASE_PARAMS = f'search/1?&app_id={APP_ID}&app_key={API_KEY}&'
    url = f'https://api.adzuna.com/v1/api/jobs/{country}/search/1'
    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'results_per_page': per_page,
        'title_only': title,
        'sort_by': 'relevance',
        'what_or': skills,
        'max_days_old': {last_posted},
    }

    headers = {
        'Accept': 'application/json'
    }

    response = requests.get(url, params=params, headers=headers)

    data = json.loads(response.text)

    df = pandas.json_normalize(data, 'results')

    # Drop duplicate rows based on the 'title' column
    df_unique = df.drop_duplicates(subset='title', keep='first')

    # get top 10 jobs
    df_unique = calculate_cosine_similarity(df_unique, resume_txt)

    job_list = []
    for _, row in df_unique.iterrows():
        job_info = {
            'title': row['title'],
            'company_name': row['company.display_name'],
            'description': row['description'],
            'redirect_url': row['redirect_url']
        }
        job_list.append(job_info)

    context = {'df_html': job_list}
    return render(request, 'companies_recommendation.html', context)