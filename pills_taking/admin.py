from django.contrib import admin
from .models import *


@admin.register(PillTaking)
class PillTakingAdmin(admin.ModelAdmin):
    pass


@admin.register(PillForm)
class PillFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(PillCurrency)
class PillCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'pill_form', 'abbreviation']


@admin.register(PillCourse)
class PillCourseAdmin(admin.ModelAdmin):
    list_display = [
        'owner', 'pill_name', 'description', 'pill_form', 'pill_currency', 'single_dose',
        'days_count', 'date_start', 'date_end', 'taking_interval', 'taking_condition'
    ]


@admin.register(TakingIntervalType)
class TakingIntervalTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'day_skip']


@admin.register(CustomIntervalTypeBinding)
class CustomIntervalTypeBindingAdmin(admin.ModelAdmin):
    list_display = ['id', 'pill_course', 'days_skip']
