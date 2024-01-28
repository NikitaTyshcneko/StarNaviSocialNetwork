from django.urls import path
from rest_framework import routers
from social_network_app.views import PostViewSet, UserActivityViewSet

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
    path('user-activity/', UserActivityViewSet.as_view({'get': 'list'}), name='user-activity'),
]

urlpatterns += router.urls
