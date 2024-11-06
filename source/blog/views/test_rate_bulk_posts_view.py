import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models.post import Post
from blog.services.rating_service import RatingService


class TestRateBulkPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        rating_service = RatingService()

        user_count = 50
        random_users = User.objects.order_by('?')[:user_count]

        post_count = 50
        random_post_ids = Post.objects.order_by('?').values_list('id', flat=True)[:post_count]

        for user in random_users:
            for post_id in random_post_ids:
                rate = random.randint(0, 5)
                rating_service.rate_post(user, post_id, rate)

        return Response(status=status.HTTP_200_OK)
