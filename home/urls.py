from django.urls import path

from .views import HomeView, AboutView, ContactView

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contacts/", ContactView.as_view(), name="contacts"),
]
