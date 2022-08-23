from rest_framework import permissions, viewsets

from api.serializers import CustomUserSerializer
from users.models import CustomUser

# from .permissions import IsOwnerOrAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

