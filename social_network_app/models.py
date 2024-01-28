from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, null=False)
    like = GenericRelation('Like')

    @property
    def get_author(self):
        return self.author.username

    @property
    def like_count(self):
        return self.like.count()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_like',
                fields=['user', 'content_type', 'object_id']
            )
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    last_request = models.DateTimeField(null=True, blank=True)

    def update_last_request(self):
        self.last_request = timezone.now()
        self.save()