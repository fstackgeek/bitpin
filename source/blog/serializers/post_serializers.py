
from rest_framework import serializers

from blog.models.post import Post


class PostSerializer(serializers.ModelSerializer):
    rating_average = serializers.FloatField()
    rating_count = serializers.IntegerField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'rating_average', 'rating_count', 'user_rating']

    def get_user_rating(self, obj):
        user = self.context['request'].user
        rating = obj.ratings.filter(user=user).first()
        return rating.value if rating else None
