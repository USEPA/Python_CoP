from django.urls import path

from .views import msgs
urlpatterns = [
    path('v0/msgs', msgs),
]


