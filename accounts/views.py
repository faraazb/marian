from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserLoginSerializer, UserSignupSerializer, UserLoginRestoreSerializer


class UserSignupView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer
    restore_serializer_class = UserLoginRestoreSerializer

    def get(self, request):
        # print(request.user)
        serializer = self.restore_serializer_class(request.user)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

