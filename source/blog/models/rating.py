from django.conf import settings
from django.db import models
from psqlextra.models import PostgresPartitionedModel
from psqlextra.types import PostgresPartitioningMethod

from blog.models.post import Post


class Rating(PostgresPartitionedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="ratings", on_delete=models.CASCADE)
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    class PartitioningMeta:
        method = PostgresPartitioningMethod.HASH
        key = ["user_id"]

    def __str__(self):
        return f'{self.user.id}: {self.value} [{self.post.title}]'
