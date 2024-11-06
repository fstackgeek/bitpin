import json
import logging

import redis
import redis.client
from celery import shared_task
from django.conf import settings

redis_client = redis.StrictRedis.from_url(settings.CELERY_BROKER_URL)


@shared_task
def enqueue_message(message):
    redis_client.rpush(QUEUE_NAME, message)


QUEUE_NAME = 'ratings_queue'
BATCH_SIZE = 1000


@shared_task
def batch_process_ratings():
    batch = []
    while True:
        message = redis_client.lpop(QUEUE_NAME)
        if message:
            batch.append(json.loads(message.decode('utf-8')))
            if len(batch) >= BATCH_SIZE:
                break
        else:
            break

    if batch:
        process_ratings(batch)


def process_ratings(ratings_batch):
    post_ratings = {}
    for rating in ratings_batch:
        post_id = rating["post_id"]
        if post_id not in post_ratings:
            post_ratings[post_id] = []
        post_ratings[post_id].append(rating)

    for post_id, ratings in post_ratings.items():
        try:
            aggregate_post_ratings(post_id, ratings)
        except Exception as e:
            logging.warning(f"process_rating failed for post {post_id}\n {e}")


def aggregate_post_ratings(post_id, ratings):
    from blog.models.post import Post

    post = Post.objects.get(id=post_id)
    if not post:
        return

    batch_stats = RunningStats().add_rating_samples(ratings).get_mean_and_std()
    post_stats = RunningStats(post.rating_details).get_mean_and_std()

    weight = calculate_weight(batch_stats, post_stats)
    if weight > 0:
        new_rating_details = RunningStats(post.rating_details).add_rating_samples(
            ratings=ratings, weight=weight)
        new_rating_average = new_rating_details.get_mean()
        new_rating_count = new_rating_details.N
        Post.objects.filter(id=post_id).update(
            rating_details=new_rating_details.to_dict(),
            rating_average=new_rating_average,
            rating_count=new_rating_count,
        )


def calculate_weight(batch_dist, base_dist):
    outlier_threshold = 5.0

    x_mean, x_std = batch_dist
    base_mean, base_std = base_dist

    if base_std == 0:
        return 1.0

    z_score = (x_mean - base_mean) / base_std
    sdr_score = x_std / base_std

    if z_score > outlier_threshold:
        logging.info(f'OUTLIER RATING DETECTED\nBatch dist:{batch_dist}\nBase dist:{base_dist}')
        return 0

    if sdr_score < 1.0 / outlier_threshold:
        logging.info(f'TARGETED RATING DETECTED\nBatch dist:{batch_dist}\nBase dist:{base_dist}')
        return 0

    weight = max(0.0, min(sdr_score / z_score, 1.0)) if z_score > 0 else 1.0

    return weight


class RunningStats:
    def __init__(self, initial={}):
        self.K = initial.get('K', 0)
        self.N = initial.get('N', 0)
        self.Ex = initial.get('Ex', 0)
        self.Ex2 = initial.get('Ex2', 0)

    def add_rating_samples(self, ratings, weight=1):
        for rate in ratings:
            if not rate['is_new']:
                self.remove_sample(rate['old_value'])
            self.add_sample(rate['value'])
        return self

    def add_sample(self, x, weight=1):
        if self.N == 0:
            self.K = x
        weighted_x = weight * (x - self.K)
        self.N += weight
        self.Ex += weighted_x
        self.Ex2 += weight * (x - self.K) ** 2
        return self

    def remove_sample(self, x, weight=1):
        if self.N == 0:
            self.K = x
        weighted_x = weight * (x - self.K)
        self.N -= weight
        self.Ex -= weighted_x
        self.Ex2 -= weight * (x - self.K) ** 2
        return self

    def get_mean(self):
        return self.K + self.Ex / self.N if self.N > 0 else 0

    def get_std(self):
        return (self.Ex2 - self.Ex ** 2 / self.N) / self.N if self.N > 1 else 0

    def get_mean_and_std(self):
        return self.get_mean(), self.get_std()

    def to_dict(self):
        return {'K': self.K, 'N': self.N, 'Ex': self.Ex, 'Ex2': self.Ex2}


if __name__ == '__main__':
    stats = RunningStats()
    stats.add_rating_samples([{'value': 5, 'old_value': 0, 'is_new': True}])
    print(stats.to_dict())
    stats.add_rating_samples([{'value': 3, 'old_value': 5, 'is_new': False}])
    print(stats.to_dict())
