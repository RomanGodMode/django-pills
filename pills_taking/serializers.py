from rest_framework import serializers

from pills_taking.models import PillTaking


class VkidListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PillTaking
        fields = ['pill_course', 'time_taking', 'is_took', 'time_took']
