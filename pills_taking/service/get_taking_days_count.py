from datetime import datetime
from math import ceil

from pills_taking.models import TakingIntervalType, PillCourse, CustomIntervalTypeBinding


def get_passed_days_count(pill_course: PillCourse):
    delta = datetime.now().date() - pill_course.date_start
    return delta.days


def _get_taking_days_count(days_count: int, taking_interval: TakingIntervalType):
    return ceil(days_count / ceil(taking_interval.day_skip + 1))


def get_taking_days_count(pill_course: PillCourse, days_count=None):
    days = days_count if days_count else pill_course.days_count

    if pill_course.taking_interval:
        return _get_taking_days_count(days, pill_course.taking_interval)

    interval_bindings = CustomIntervalTypeBinding.objects.filter(pill_course=pill_course).order_by('id')

    takings = 0

    while days > 0:
        for bind in interval_bindings:
            days -= 1
            if not days > 0:
                break
            days -= bind.days_skip
            takings += 1

    return takings
