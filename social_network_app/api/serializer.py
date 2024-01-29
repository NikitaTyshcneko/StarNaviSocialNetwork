from rest_framework import serializers
from social_network_app.models import Post, Like, UserProfile


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'create_at', 'like_count']


class LikeAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    like_count = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['date', 'like_count']


class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = UserProfile
        fields = ['user', 'last_login', 'last_request']