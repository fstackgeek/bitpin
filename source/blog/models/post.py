import uuid

from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating_average = models.FloatField(default=0)
    rating_count = models.FloatField(default=0)
    rating_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
