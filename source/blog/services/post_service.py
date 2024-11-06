from rest_framework.pagination import CursorPagination
from rest_framework.request import Request

from blog.models.post import Post


class PostPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'


class PostService:
    def get_posts(self, request: Request):
        posts_queryset = Post.objects.all()
        paginator = PostPagination()
        posts = paginator.paginate_queryset(posts_queryset, request)
        return posts, paginator
