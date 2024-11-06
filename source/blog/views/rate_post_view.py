
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.services.rating_service import RatingService


class RatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        try:
            value = int(request.data.get('value'))
        except Exception:
            value = None

        if value is None:
            return Response({'error': 'Value is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not (0 <= value <= 5):
            return Response({'error': 'Rate should be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        rating_service = RatingService()
        successful = rating_service.rate_post(user, post_id, value)

        if successful:
            return Response(status=status.HTTP_200_OK)

        return Response({'error': 'Failed to rate post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def post_id_key(group, request):
    post_id = request.resolver_match.kwargs.get('post_id', '')
    return post_id
