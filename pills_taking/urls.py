from django.urls import path
from .views import *

urlpatterns = [
    path('vkids/', TakingListView.as_view())
]
