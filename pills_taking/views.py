from datetime import datetime

from rest_framework import generics, viewsets, mixins

from pills_taking.models import PillTaking, PillCourse
from pills_taking.serializers import VkidListSerializer, ActiveCoursesSerializer, CompletedCoursesSerializer, \
    DetailCourseSerializer


class TakingListView(generics.ListAPIView):
    serializer_class = VkidListSerializer

    def get_queryset(self):
        return PillTaking.objects.filter(pill_course__owner=self.request.user)


class ActiveCoursesListView(generics.ListAPIView):
    serializer_class = ActiveCoursesSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user, date_end__gte=datetime.now())


class CompletedCoursesListView(generics.ListAPIView):
    serializer_class = CompletedCoursesSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user, date_end__lt=datetime.now())


class DetailCourseView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = DetailCourseSerializer

    def get_queryset(self):
        return PillCourse.objects.filter(owner=self.request.user)

# Все мои приёмы на сегодня
# [
#     {
#         Время принятия
#         Принят
#         Course: {
#               id
#                "Название таблетки",
#                "condition", dose, currency_name,
#
#         }
#     }
# ]
#
# [
#     {
#         "Название таблетки",
#         "дата начала",
#         "дата конца",
#         "пройденное Кол-во дней",
#         "Кол-во дней",
#         "пройденное Кол-во приёмов",
#         "Кол-во приёмов",
#     }
# ]
#
# [
#     {
#         "Название таблетки",
#         "дата начала",
#         "дата конца",
#         "Форма"
#     }
# ]
# # TODO: Формочка курса
#
#     {
#         Всё
#         Тип
#         Куренси { Время которое нада }
#     }

# Действия
# Круд Курса
# Цеплять приёмы к курсу
