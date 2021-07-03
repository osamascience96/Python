from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("osama", views.osama, name="osama"),
    path("<str:name>", views.greet, name="greet")
]