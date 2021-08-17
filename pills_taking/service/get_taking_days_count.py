from math import ceil

from pills_taking.models import TakingIntervalType


def get_taking_days_count(days_count: int, taking_interval: TakingIntervalType):
    return ceil(days_count / ceil(taking_interval.day_skip + 1))
