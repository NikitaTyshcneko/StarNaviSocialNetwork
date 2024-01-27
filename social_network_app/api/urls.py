from rest_framework import routers
from social_network_app.views import PostViewSet

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
]

urlpatterns += router.urls
