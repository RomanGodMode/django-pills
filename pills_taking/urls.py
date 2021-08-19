from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'pill-forms', PillFormViewSet)
router.register(r'pill-currencies', PillCurrencyViewSet)

urlpatterns = [
    path('vkids/', TakingListView.as_view()),
    path('active-courses/', ActiveCoursesListView.as_view()),
    path('completed-courses/', CompletedCoursesListView.as_view()),
    path('courses/<int:pk>/', DetailCourseView.as_view()),
    path('courses/create/', CreateCourseView.as_view()),
    path('courses/update/<int:pk>/', UpdateCourseView.as_view()),
    path('', include(router.urls))
]
