from django.urls import path

from . import views

# adding namespace
app_name = 'recon'

urlpatterns =[
    path("", views.ReconciliationFileUploadAPI.as_view(), name="upload"),
    path("upload/", views.ReconciliationFileUploadAPI.as_view(), name="upload"),
    path("report/<str:req_hash>/", views.ReconciliationFileReportAPI.as_view(), name="report"),
    path("report/<str:req_hash>/<str:file_format>/", views.ReconciliationFileReportAPI.as_view(), name="report_with_format"),
]