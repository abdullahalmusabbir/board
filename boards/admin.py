from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'active', 'date_of_birth', 'joined_at']
    list_filter   = ['active']
    search_fields = ['user__username', 'user__email']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ['name', 'color']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display   = ['title', 'user', 'status', 'priority', 'task_date', 'due_date', 'order']
    list_filter    = ['status', 'priority', 'task_date']
    search_fields  = ['title', 'user__username']
    filter_horizontal = ['tags']
    ordering       = ['order', 'created_at']


@admin.register(AnnotationImage)
class AnnotationImageAdmin(admin.ModelAdmin):
    list_display  = ['title', 'user', 'order', 'uploaded_at']
    search_fields = ['title', 'user__username']
    ordering      = ['order', 'uploaded_at']


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display  = ['label', 'image', 'color', 'created_at']
    search_fields = ['label', 'image__title']
    ordering      = ['created_at']