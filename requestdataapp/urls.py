from django.urls import path

from .views import process_get_view, user_form, file_form

app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_get_view, name="get_view"),
    path("bio/", user_form, name="user-form"),
    path("file/", file_form, name="file-form"),
]