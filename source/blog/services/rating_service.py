
import json

from django.db import transaction

from blog.models.post import Post
from blog.models.rating import Rating
from blog.tasks import enqueue_message


class RatingService:
    def rate_post(self, user, post_id, rate):
        post = Post.objects.get(id=post_id)

        if post is None:
            return False

        with transaction.atomic():
            previous_rate = 0
            try:
                previous_rate = Rating.objects.get(user=user, post=post).value
            except Rating.DoesNotExist:
                pass

            new_rating, is_new = Rating.objects.update_or_create(
                user=user,
                post=post,
                defaults={'value': rate}
            )

            value_change = rate - previous_rate

            if value_change:
                post_id_string = str(post_id)
                try:
                    rating_data = {
                        'user_id': user.id,
                        'post_id': post_id_string,
                        'value': rate,
                        'old_value': previous_rate,
                        'is_new': is_new,
                        'timestamp': new_rating.timestamp.isoformat()
                    }
                    message = json.dumps(rating_data)
                    enqueue_message.delay(message)
                except Exception as e:
                    print('Failed to send rating to kafka', e)

            return True
