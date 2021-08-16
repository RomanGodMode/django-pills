from rest_framework import generics, viewsets

from pills_taking.models import PillTaking
from pills_taking.serializers import VkidListSerializer


class TakingListView(generics.ListAPIView):
    serializer_class = VkidListSerializer

    def get_queryset(self):
        return PillTaking.objects.filter(pill_course__owner=self.request.user)

# # TODO: Все мои приёмы на сегодня
# [
#     {
#         "Название таблетки",
#         "Описание курса",
#     }
# ]
#
# # TODO: Активные курсы
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
# # TODO: Завершённые курсы
# [
#     {
#         "Название таблетки",
#         "дата начала",
#         "дата конца",#
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
