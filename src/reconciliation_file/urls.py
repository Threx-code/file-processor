from django.urls import path

from . import views

# adding namespace
app_name = 'recon'

urlpatterns =[
    path("", views.ReconciliationFileUploadApi.as_view(), name="upload"),
    path("upload/", views.ReconciliationFileUploadApi.as_view(), name="upload"),
]