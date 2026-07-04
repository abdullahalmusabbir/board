from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from boards.models import *
from boards.serializers import *



def set_profile_active(user, value: bool):

    Profile.objects.filter(user=user).update(active=value)


def user_data(user):

    profile = getattr(user, 'admin_profile', None)
    return {
        'id'        : user.id,
        'username'  : user.username,
        'email'     : user.email,
        'first_name': user.first_name,
        'last_name' : user.last_name,
        'avatar'    : profile.avatar.url if profile and profile.avatar else None,
        'active'    : profile.active     if profile else False,
    }

#  AUTH──────────────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email    = request.data.get('email', '').strip()
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Account is disabled.'},
                status=status.HTTP_403_FORBIDDEN
            )

        login(request, user)
        set_profile_active(user, True)      

        return Response(
            {'message': 'Login successful.', 'user': user_data(user)},
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        set_profile_active(request.user, False)   
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(user_data(request.user), status=status.HTTP_200_OK)

#  TAGS──────────────────────────────────────────────────────────────────────────────

class TagListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(TagSerializer(Tag.objects.all(), many=True).data)

    def post(self, request):
        s = TagSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response(TagSerializer(get_object_or_404(Tag, pk=pk)).data)

    def put(self, request, pk):
        s = TagSerializer(get_object_or_404(Tag, pk=pk), data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        get_object_or_404(Tag, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#  TASKS──────────────────────────────────────────────────────────────────────────────

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        # optional filters from query params
        if date := request.query_params.get('date'):
            tasks = tasks.filter(task_date=date)
        if s := request.query_params.get('status'):
            tasks = tasks.filter(status=s)
        if p := request.query_params.get('priority'):
            tasks = tasks.filter(priority=p)

        return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request):
        s = TaskSerializer(data=request.data)
        if s.is_valid():
            s.save(user=request.user)
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk, user=self.request.user)

    def get(self, request, pk):
        return Response(TaskSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        s = TaskSerializer(self.get_object(pk), data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        s = TaskSerializer(self.get_object(pk), data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskBulkOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        items = request.data
        if not isinstance(items, list):
            return Response({'error': 'Expected a list.'}, status=status.HTTP_400_BAD_REQUEST)

        updated = []
        for item in items:
            task = get_object_or_404(Task, pk=item.get('id'), user=request.user)
            task.order  = item.get('order',  task.order)
            task.status = item.get('status', task.status)
            task.save(update_fields=['order', 'status'])
            updated.append(task.id)

        return Response({'updated': updated}, status=status.HTTP_200_OK)

#  ANNOTATION — Images──────────────────────────────────────────────────────────────────────────────

class AnnotationImageListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def get(self, request):
        images = AnnotationImage.objects.filter(user=request.user)
        return Response(
            AnnotationImageSerializer(images, many=True, context={'request': request}).data
        )

    def post(self, request):
        s = AnnotationImageSerializer(data=request.data, context={'request': request})
        if s.is_valid():
            s.save(user=request.user)
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnotationImageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return get_object_or_404(AnnotationImage, pk=pk, user=self.request.user)

    def get(self, request, pk):
        return Response(
            AnnotationImageSerializer(self.get_object(pk), context={'request': request}).data
        )

    def patch(self, request, pk):
        s = AnnotationImageSerializer(
            self.get_object(pk), data=request.data, partial=True, context={'request': request}
        )
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#  ANNOTATION — Polygons──────────────────────────────────────────────────────────────────────────────

class PolygonListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_image(self, image_pk):
        return get_object_or_404(AnnotationImage, pk=image_pk, user=self.request.user)

    def get(self, request, image_pk):
        polygons = self.get_image(image_pk).polygons.all()
        return Response(PolygonSerializer(polygons, many=True).data)

    def post(self, request, image_pk):
        image = self.get_image(image_pk)
        s = PolygonSerializer(data={**request.data, 'image': image.pk})
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class PolygonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Polygon, pk=pk, image__user=self.request.user)

    def get(self, request, pk):
        return Response(PolygonSerializer(self.get_object(pk)).data)

    def patch(self, request, pk):
        s = PolygonSerializer(self.get_object(pk), data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PolygonBulkSaveView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, image_pk):
        image = get_object_or_404(AnnotationImage, pk=image_pk, user=request.user)

        raw = request.data.get('polygons', [])
        if not isinstance(raw, list):
            return Response(
                {'error': 'Expected a list under "polygons".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image.polygons.all().delete()   

        created = []
        for poly in raw:
            s = PolygonSerializer(data={**poly, 'image': image.pk})
            if s.is_valid():
                s.save()
                created.append(s.data)
            else:
                return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'saved': created}, status=status.HTTP_201_CREATED)
    
