from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]