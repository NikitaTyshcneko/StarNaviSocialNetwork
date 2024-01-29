import functools

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_network_app.models import Like


def error_handler(expect_error, error_message):
    def decorator(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
                return Response(data=data, status=status.HTTP_200_OK)
            except expect_error:
                return Response({'details': error_message}, status=status.HTTP_400_BAD_REQUEST)

        return inner_function

    return decorator


class LikeModelMixin:

    @error_handler(IntegrityError, 'Content is already liked by the user.')
    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        content = self.get_object()
        user = request.user

        like = Like.objects.create(user=user, content_object=content)
        like.save()
        return {'status': 'liked'}

    @error_handler(ObjectDoesNotExist, 'Content not liked by the user.')
    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike(self, request, pk=None):
        content = self.get_object()
        user = request.user


        like = Like.objects.get(user=user, object_id=content.id)
        like.delete()
        return {'status': 'unliked'}
