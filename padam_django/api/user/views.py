from rest_framework.viewsets import ModelViewSet
from .serializer import UserSerializer
from ...apps.users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
