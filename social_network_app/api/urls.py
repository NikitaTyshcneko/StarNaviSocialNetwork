from django.urls import path
from rest_framework import routers
from social_network_app.views import PostViewSet, UserActivityViewSet, LikeAnalyticsViewSet

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
router.register(r'like-analytic', LikeAnalyticsViewSet, basename='like-analytic')
router.register(r'user-activity', UserActivityViewSet, basename='user-activity')

urlpatterns = [
]

urlpatterns += router.urls
