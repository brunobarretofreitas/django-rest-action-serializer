from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework.test import APITestCase
from rest_framework.response import Response

from .serializers import UserSerializer, NoActionConfigUserSerializer

class DRATestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            username='myuser',
            email='myuser@email.com',
            first_name='my',
            last_name='user',
            password='mypassword'
        )

    def test_list_action_not_retrieve_fullname_attribute(self):
        """
        This attribute is configured to display only in retrieve action
        on UserSerializer
        """
        response: Response = self.client.get(reverse('user-list'))
        
        user_data = response.data[0]

        self.assertNotIn('fullname', user_data.keys())

    def test_list_action_retrieves_username_attribute(self):
        """
        This attribute is configured to display only in list action
        on UserSerializer
        """
        response: Response = self.client.get(reverse('user-list'))
        
        user_data = response.data[0]

        self.assertIn('username', user_data.keys())

    def test_list_action_not_retrieves_fullname_attribute(self):
        """
        fullname is a SerializerMethodField configured to display only in retrive action
        """
        response: Response = self.client.get(reverse('user-list'))
        
        user_data = response.data[0]

        self.assertNotIn('fullname', user_data.keys())

    def test_retrieve_action_displays_fullname_attribute_and_no_username(self):
        """
        This attribute is configured to display only in list action
        on UserSerializer
        """
        response: Response = self.client.get(
            reverse(
                'user-detail',
                kwargs={'pk': self.user.id}
            )
        )
        
        user_data = response.data

        self.assertIn('fullname', user_data.keys())
        self.assertNotIn('username', user_data.keys())

    def test_no_view_passed_to_serializer(self):
        """
        When using the serializer manually, it is not possible
        to determine the action (list, retrive), so the default
        fields are always returned
        """
        serializer_instance = UserSerializer(self.user)
        serializer_data = serializer_instance.data

        self.assertIn('username', serializer_data)
    
    def test_no_action_fields_map_provided(self):
        """
        When the attribute `action_fields_map` is not provided,
        the default fields are always returned
        """
        response: Response = self.client.get(
            reverse(
                'user-no-action-config-detail',
                kwargs={'pk': self.user.id}
            )
        )

        self.assertIn('username', response.data.keys())