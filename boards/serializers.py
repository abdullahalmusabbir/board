from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model  = Profile
        fields = ['id', 'user', 'active', 'date_of_birth', 'avatar', 'joined_at']


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# ── Task Board ─────────────────────────────────────────────────────────────────

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'color']


class TaskSerializer(serializers.ModelSerializer):
    tags     = TagSerializer(many=True, read_only=True)
    tag_ids  = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False
    )

    class Meta:
        model  = Task
        fields = [
            'id', 'title', 'description',
            'priority', 'status',
            'task_date', 'due_date',
            'order', 'tags', 'tag_ids',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# ── Annotation ─────────────────────────────────────────────────────────────────

class PolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Polygon
        fields = ['id', 'image', 'label', 'color', 'points', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AnnotationImageSerializer(serializers.ModelSerializer):
    polygons = PolygonSerializer(many=True, read_only=True)

    class Meta:
        model  = AnnotationImage
        fields = ['id', 'title', 'image', 'order', 'uploaded_at', 'polygons']
        read_only_fields = ['uploaded_at']