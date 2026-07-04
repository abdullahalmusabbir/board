"""
URL configuration for board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('iloveumusabbir/', admin.site.urls),
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('auth/signup/',  views.SignupView.as_view(),   name='signup'),    
    path('auth/login/',   views.LoginView.as_view(),  name='login'),
    path('auth/logout/',  views.LogoutView.as_view(), name='logout'),
    path('auth/me/',      views.MeView.as_view(),     name='me'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ── Tags ──────────────────────────────────────────────────────────────────
    path('tags/',         views.TagListCreateView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(),   name='tag-detail'),

    # ── Tasks ─────────────────────────────────────────────────────────────────
    path('tasks/',                views.TaskListCreateView.as_view(), name='task-list'),
    path('tasks/reorder/',        views.TaskBulkOrderView.as_view(),  name='task-reorder'),
    path('tasks/<int:pk>/',       views.TaskDetailView.as_view(),     name='task-detail'),

    # ── Annotation Images ─────────────────────────────────────────────────────
    path('images/',               views.AnnotationImageListCreateView.as_view(), name='image-list'),
    path('images/<int:pk>/',      views.AnnotationImageDetailView.as_view(),     name='image-detail'),

    # ── Polygons ──────────────────────────────────────────────────────────────
    path('images/<int:image_pk>/polygons/',        views.PolygonListCreateView.as_view(), name='polygon-list'),
    path('images/<int:image_pk>/polygons/bulk/',   views.PolygonBulkSaveView.as_view(),   name='polygon-bulk'),
    path('polygons/<int:pk>/',                     views.PolygonDetailView.as_view(),     name='polygon-detail'),
]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]