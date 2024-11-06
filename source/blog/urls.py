from django.urls import path
from django_ratelimit.decorators import ratelimit

from blog.views.post_list_view import PostListView
from blog.views.rate_post_view import RatePostView, post_id_key
from blog.views.test_create_bulk_posts_view import TestCreateBulkPostsView
from blog.views.test_rate_bulk_posts_view import TestRateBulkPostsView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<uuid:post_id>/rate/', ratelimit(key=post_id_key, rate='1000/s',
         method='POST', block=True)(RatePostView.as_view()), name='rate-post'),
    path('posts/test/bulkpost/', TestCreateBulkPostsView.as_view(), name='create-bulk-posts'),
    path('posts/test/bulkrate/', TestRateBulkPostsView.as_view(), name='rate-bulk-posts'),
]
