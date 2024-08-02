from rest_framework import status
from sms.models import List, User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from sms.serializers import UserSerializer, ListSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        list_obj = self.get_object()
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        list_obj.users.add(user)
        return Response({"status": "user added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_user(self, request, pk=None):
        list_obj = self.get_object()
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        list_obj.users.remove(user)
        return Response({"status": "user removed"}, status=status.HTTP_200_OK)
