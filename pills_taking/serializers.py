from datetime import datetime
from math import ceil

from rest_framework import serializers

from pills_taking.models import PillTaking, PillCourse, PillForm
from pills_taking.service.get_taking_days_count import get_taking_days_count


class PillFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PillForm
        fields = ['name', 'icon']


class ModestCourseSerializer(serializers.ModelSerializer):
    pill_form = PillFormSerializer(read_only=True)

    class Meta:
        model = PillCourse
        fields = ['id', 'pill_name', 'taking_condition', 'pill_currency', 'single_dose', 'pill_form']


class VkidListSerializer(serializers.ModelSerializer):
    pill_course = ModestCourseSerializer(read_only=True)

    class Meta:
        model = PillTaking
        fields = ['pill_course', 'time_taking', 'is_took']


# noinspection PyMethodMayBeStatic
class ActiveCoursesSerializer(serializers.ModelSerializer):
    pill_form = PillFormSerializer(read_only=True)
    completed_days_count = serializers.SerializerMethodField()
    pill_taking_count = serializers.SerializerMethodField()
    completed_pill_taking_count = serializers.SerializerMethodField()

    class Meta:
        model = PillCourse
        fields = [
            'id', 'pill_name', 'date_start', 'date_end',
            'pill_currency', 'pill_form', 'days_count', 'pill_form',
            'completed_days_count', 'pill_taking_count', 'completed_pill_taking_count'
        ]

    def get_completed_days_count(self, instance):
        delta = datetime.now().date() - instance.date_start
        return delta.days

    def get_pill_taking_count(self, instance: PillCourse):
        taking_days_count = get_taking_days_count(instance.days_count, instance.taking_interval)
        return PillTaking.objects.filter(pill_course=instance).count() * taking_days_count

    def get_completed_pill_taking_count(self, instance: PillCourse):
        completed_days_count = self.get_completed_days_count(instance)
        completed_taking_days_count = get_taking_days_count(completed_days_count, instance.taking_interval)

        takings = PillTaking.objects.filter(pill_course=instance)
        takings_per_day = takings.count()
        past_takings_count = takings_per_day * completed_taking_days_count
        today_takings_count = takings.filter(is_took=True).count()

        return past_takings_count + today_takings_count
