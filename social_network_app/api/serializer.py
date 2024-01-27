from rest_framework import serializers
from social_network_app.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'
