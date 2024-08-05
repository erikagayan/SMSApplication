from rest_framework import status
from sms.models import List, User, SMS
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from sms.synchronization import synchronize_list
from sms.serializers import UserSerializer, ListSerializer, SMSSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        list_obj = self.get_object()  # get an instance of List
        user_id = request.data.get("user_id")  # get user id

        try:
            user = User.objects.get(id=user_id)  # try to find user
            list_obj.users.add(user)
            list_obj.save()
            return Response({'status': 'user added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def remove_user(self, request, pk=None):
        list_obj = self.get_object()
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            list_obj.users.remove(user)
            list_obj.save()
            return Response({"status": "user removed"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def send_sms(self, request, pk=None):
        list_obj = self.get_object()
        sender_id = request.data.get("sender_id")
        content = request.data.get("content")

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)

        for user in list_obj.users.all():
            sms = SMS.objects.create(sender=sender, receiver=user, content=content)
            sms.save()

        return Response({"status": "SMS sent"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_sms(self, request, pk=None):
        list_obj = self.get_object()
        sms_list = SMS.objects.filter(receiver__in=list_obj.users.all())
        serializer = SMSSerializer(sms_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def synchronize(self, request, pk=None):
        endpoint = request.data.get("endpoint")
        params = request.data.get("params", {})

        try:
            synchronize_list(pk, endpoint, params)
            return Response({"status": "Synchronization completed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
