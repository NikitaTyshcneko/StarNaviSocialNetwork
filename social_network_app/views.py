from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from social_network_app.api.filter import LikeAnalyticsFilter
from social_network_app.api.mixins import LikeModelMixin
from social_network_app.api.serializer import PostSerializer, UserActivitySerializer, LikeAnalyticsSerializer
from social_network_app.models import Post, UserProfile, Like
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate


def register_request(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["confirm_password"]:
            is_user_exists = User.objects.filter(username=request.POST["username"]).exists()
            if is_user_exists:
                raise ValidationError('This username is already used!')
            else:
                User.objects.create_user(username=request.POST["username"],
                                         password=request.POST["password"])
                return redirect('/login/')
    form = UserCreationForm()
    return render(request, 'register.html', {'register_form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/api/v1/post/')
    form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': form})


def logout_request(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    user_profile.last_login = timezone.now()
    user_profile.save()
    logout(request)
    return redirect('/login/')


# Create your views here.
class PostViewSet(ModelViewSet, LikeModelMixin):
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserActivityViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivitySerializer
    queryset = UserProfile.objects.all()

    def get(self):
        user_profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        serializer = UserActivitySerializer(user_profile)
        return Response(serializer.data)


class LikeAnalyticsViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeAnalyticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikeAnalyticsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            created_at__date__gte=self.request.query_params.get('date_from'),
            created_at__date__lte=self.request.query_params.get('date_to')
        )
        queryset = queryset.annotate(date=TruncDate('created_at')).values('date')
        queryset = queryset.annotate(like_count=Count('id')).order_by('date')
        return queryset
