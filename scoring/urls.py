from django.urls import path

from . import views

urlpatterns = [
    path('create_score', views.create_score, name="create_score"),
]
