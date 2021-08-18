from django.urls import path
from .views import *

urlpatterns = [
    path('vkids/', TakingListView.as_view()),
    path('active-courses/', ActiveCoursesListView.as_view()),
    path('completed-courses/', CompletedCoursesListView.as_view()),
    path('courses/<int:pk>/', DetailCourseView.as_view())

]
