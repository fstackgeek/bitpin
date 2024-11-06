from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.serializers.post_serializers import PostSerializer
from blog.services.post_service import PostService


class PostPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'


class PostListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = PostService()
        posts, paginator = service.get_posts(request=request)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({
            'posts': serializer.data,
            'next_cursor': paginator.get_next_link(),
            'previous_cursor': paginator.get_previous_link(),
        })
