from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from pills_taking.models import PillTaking, PillCourse, PillForm, PillCurrency
from pills_taking.serializers import VkidListSerializer, ActiveCoursesSerializer, CompletedCoursesSerializer, \
    DetailCourseSerializer, CreateCourseSerializer, PillFormSerializer, CurrencySerializer, UpdateCourseSerializer


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


class UpdateCourseView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCourseSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user)


class PillFormViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PillForm.objects.all()
    serializer_class = PillFormSerializer


class PillCurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PillCurrency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['pill_form']
