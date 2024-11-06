import random
import string

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import SignUpSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestSignUpBulkUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        count = 50
        for i in range(count):
            user = {'username': random_string(), 'password': random_string()}
            serializer = SignUpSerializer(data=user)
            if serializer.is_valid():
                serializer.save()
        return Response(status=status.HTTP_200_OK)


def random_string(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
