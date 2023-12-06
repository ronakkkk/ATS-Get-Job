from django.urls import path
from django.contrib import admin
from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.index, name="index"),
    path('admin/', admin.site.urls),
    path('checkUserDetails', views.checkUserDetails, name="Check Data"),
    path('signUpUser', views.signUpUser, name="Sign Up"),
    path('create_user', views.create_user, name="Insert Login Data"),
    path('upload_resume/', views.upload_resume , name='upload_resume'),
    path('upload_resume/uploadS3', views.upload_to_s3 , name='uploadS3'),
    path('upload_resume/getResume', views.get_s3_file , name='getResumeFromS3'),
    path('getJobs', views.getJobs, name='getJobs'),
    path('upload_resume/compare_resume', views.compare_resume, name="compareResume"),
    path('', include(router.urls)),
]
