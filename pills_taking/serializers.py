from datetime import datetime
from math import ceil

from rest_framework import serializers

from pills_taking.models import PillTaking, PillCourse, PillForm, PillCurrency, TakingIntervalType, \
    CustomIntervalTypeBinding
from pills_taking.service.get_taking_days_count import get_taking_days_count, get_passed_days_count


class PillFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PillForm
        fields = ['id', 'name', 'icon']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PillCurrency
        fields = ['id', 'name', 'abbreviation']


class TakingIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakingIntervalType
        fields = ['id', 'title', 'day_skip']


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
        return get_passed_days_count(instance)

    def get_pill_taking_count(self, instance: PillCourse):
        taking_days_count = get_taking_days_count(instance)
        return PillTaking.objects.filter(pill_course=instance).count() * taking_days_count

    def get_completed_pill_taking_count(self, instance: PillCourse):
        completed_days_count = get_passed_days_count(instance)
        completed_taking_days_count = get_taking_days_count(instance, days_count=completed_days_count)
        takings = PillTaking.objects.filter(pill_course=instance)
        takings_per_day = takings.count()
        past_takings_count = takings_per_day * completed_taking_days_count
        today_takings_count = takings.filter(is_took=True).count()

        return past_takings_count + today_takings_count


class CompletedCoursesSerializer(serializers.ModelSerializer):
    pill_form = PillFormSerializer(read_only=True)

    class Meta:
        model = PillCourse
        fields = ['pill_name', 'date_start', 'date_end', 'pill_form']


class DetailCourseSerializer(serializers.ModelSerializer):
    pill_form = PillFormSerializer(read_only=True)
    pill_currency = CurrencySerializer(read_only=True)
    taking_interval = TakingIntervalSerializer(read_only=True)

    class Meta:
        model = PillCourse
        fields = [
            'id', 'pill_name', 'description', 'taking_condition',
            'date_start', 'days_count', 'single_dose',
            'pill_form', 'pill_currency', 'taking_interval'
        ]


class CustomIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomIntervalTypeBinding
        fields = ['days_skip']


class CreateCourseSerializer(serializers.ModelSerializer):
    # interval_binds = serializers.ListField(child=serializers.IntegerField(), default=None)
    # interval_binds = serializers.ListField(child=serializers.IntegerField(), default=None)
    interval_binds = CustomIntervalSerializer(many=True, default=None)

    class Meta:
        model = PillCourse
        fields = [
            'pill_name', 'description', 'taking_condition', 'date_start', 'days_count', 'single_dose',
            'pill_form', 'pill_currency', 'taking_interval', 'interval_binds'
        ]

    def validate(self, attrs):
        if not attrs['interval_binds'] and not attrs.get('taking_interval', None):
            raise serializers.ValidationError("Должен быть выбран хоть какой-то интервал")
        if attrs['interval_binds'] and attrs.get('taking_interval', None):
            raise serializers.ValidationError("Нельзя выбрать 2 типа выбора интервала")

        return super().validate(attrs)

    def create(self, validated_data):
        custom_interval_binds = validated_data.pop('interval_binds')

        course = PillCourse.objects.create(**validated_data, owner=self.context['request'].user)

        if custom_interval_binds:
            course.interval_binds.set([
                CustomIntervalTypeBinding.objects.create(pill_course=course, days_skip=interval['days_skip'])
                for interval in custom_interval_binds
            ])

        return course
