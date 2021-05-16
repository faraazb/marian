from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from pickups.models import Pickup
from pickups.serializers import PickupSerializer


class PickupListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    model = Pickup
    permission_classes = (IsAuthenticated, )
    # queryset = Pickup.objects.all()
    serializer_class = PickupSerializer

    def get(self, request):
        serializer = self.get_serializer(Pickup.objects.filter(is_done=False, is_active=True), many=True)
        return Response(serializer.data)


class PickupDetailViewProtected(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PickupSerializer

    def get_object(self, pk):
        try:
            return Pickup.objects.get(pk=pk)
        except Pickup.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        pickup_request = self.get_object(pk)
        serializer = self.serializer_class(pickup_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pickup_request = self.get_object(pk)
        pickup_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PickupDetailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PickupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

