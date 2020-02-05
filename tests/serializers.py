from django.contrib.auth.models import User
from rest_framework import serializers

from dra.serializers import ActionSerializer

class UserSerializer(ActionSerializer,
                     serializers.ModelSerializer):

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name'
        )
        action_fields_map = {
            'retrieve': {
                'fields': fields + (
                    ('fullname', serializers.SerializerMethodField()),
                ),
                'exclude': ('username',)
            }
        }

class NoActionConfigUserSerializer(UserSerializer, ActionSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name'
        )