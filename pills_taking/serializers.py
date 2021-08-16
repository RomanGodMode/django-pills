from rest_framework import serializers

from pills_taking.models import PillTaking, PillCourse, PillForm


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
