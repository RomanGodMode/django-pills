from datetime import datetime

from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from pills_taking.models import PillTaking, PillCourse
from pills_taking.serializers import VkidListSerializer, ActiveCoursesSerializer, CompletedCoursesSerializer, \
    DetailCourseSerializer, CreateCourseSerializer


class TakingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VkidListSerializer

    def get_queryset(self):
        return PillTaking.objects.filter(pill_course__owner=self.request.user)


class ActiveCoursesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveCoursesSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user, date_end__gte=datetime.now())


class CompletedCoursesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompletedCoursesSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user, date_end__lt=datetime.now())


class DetailCourseView(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailCourseSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user)


class CreateCourseView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCourseSerializer

# Действия
# Круд Курса
# Цеплять приёмы к курсу
