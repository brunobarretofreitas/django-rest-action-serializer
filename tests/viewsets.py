from django.contrib.auth import models
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer, NoActionConfigUserSerializer

class UserModelViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

class UserNoActionConfigModelViewSet(UserModelViewSet):
    serializer_class = NoActionConfigUserSerializer