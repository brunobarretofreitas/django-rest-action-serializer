# django-rest-action-serializer
A Django app that provides a serializer that allows You to customize the fields according to the action provided without the need to create other serializers.

# Quickstart

As an example, let's suppose You have a ModelViewSet which You need to display different fields in the list action and in the retrieve action. Without django-rest-action-serializer, You would do:

```python
class SerializerForList(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = ('url', 'name', 'age')
    

class SerializerForDetail(SerializerForList):
    stories = StorySerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('name', 'age', 'stories')
    

class UserModelViewSet(ModelViewSet):
    serializer_class = SerializerForList
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.detail:
            return SerializerForDetail
        
        return super().get_serializer_class()
```

A lot of code, right? See how It's easy to do it with django-rest-action-serializer

```python
from dra.serializers import ActionSerializer

class UserSerializer(serializers.ModelSerializer,
                     ActionSerializer):
    
    class Meta:
        model = User
        fields = ('url', 'name', 'age',)
        action_fields_map: {
            'retrieve': {
                'fields': fields + ('stories',),
                'exclude': ('url',),
                'custom_fields': {
                    'stories': StorySerializer(
                        read_only=True,
                        many=True
                    )
                }
            }
        }
        
class UserModelViewSet(ModelViewSet):
    serializer_class = SerializerForList
    queryset = User.objects.all()
```

So, all You need to do is to make your serializer class innherit the ActionSerializer from django-rest-action-serializer and set in it's Meta class the **action_fields_map** attribute, with the following structure:

```python
class Meta:
    ...
    action_fields_map = {
      '<action name (retrieve, list, delete)>': {
        'fields': (<all the fields you want to display/provide>),
        'exclude': (<all the fields you want to remove from the fields attribute>),
        'custom_fields': { # All the fields you need to customize
          '<field_name>': <Serializer or Serializer Field Class (ex: UserSerializer, SerializerMethodField)>
        }
      }
    }
```

# Contribution
Feel free to contribute to this project :D Just open an issue or a pull-request
