from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models.post import Post


class TestCreateBulkPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        count = 50
        last_index = Post.objects.count()
        for i in range(last_index + 1, last_index + 1 + count):
            Post(title=f'Title {i}', content=f'This is the content of the post {i}').save()
        return Response(status=status.HTTP_200_OK)
