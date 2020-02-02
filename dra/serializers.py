from rest_framework import serializers

class ActionSerializer(serializers.Serializer):
    """
    Mixin to add action_fields_map attribute to serializer's Meta.
    ex: 
        class Meta:
            fields = ('url', 'user',)
            action_fields_map = {
                'retrieve': {
                    'fields': fields + ('checked',)
                    'exclude_fields': ['url'],
                    'custom_fields': {
                        'stories': StorySerializer(read_only=True, many=True)
                    }
                }
            }
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        meta = getattr(self, 'Meta', None)
        # attribute to configure the action fields mapping
        self.action_fields_map: dict = getattr(meta, 'action_fields_map', None)
        self._validate_action_fields_map(self.action_fields_map)

    def _validate_action_fields_map(self, action_fields_map: dict):
        if action_fields_map:
            # Asserting action_fields_map is a dictionary.
            assert isinstance(action_fields_map, dict), \
                'The attribute action_fields_map must be instance of dict'
            
            # Iterating over the actions
            for action, config in action_fields_map.items():
                assert isinstance(action, str), \
                    'The action name must be a string not {}'.format(type(action).__name__)

                assert isinstance(config, dict), \
                    'The configuration for `{}` action must be a dictionary not {}'.format(action, type(config).__name__)

                fields = config.get('fields', None)
                exclude = config.get('exclude', None)
                custom_fields = config.get('custom_fields', None)
                
                if fields is not None:
                    assert isinstance(fields, (list, tuple)), \
                        'The `fields` must be a list. Got `{}`'.format(type(fields).__name__)

                if exclude is not None:
                    assert isinstance(exclude, (list, tuple)), \
                        '`exclude` attribute must be a list'
                
                if custom_fields is not None:
                    assert isinstance(custom_fields, dict), \
                        '`custom_fields` must be a dictionary'

    def _get_action_config(self, current_action: str, action_fields_map: dict) -> dict:
        return action_fields_map.get(current_action, None)

    # Overriding to include the new fields or to remove fields
    def get_field_names(self, declared_fields, info):
        # Checking if the view is passed to the serializer instance
        if not (self.context and self.context.get('view', None)):
            return super().get_field_names(declared_fields, info)

        if self.action_fields_map is None:
            return super().get_field_names(declared_fields, info)
        
        current_action = self.context.get('view').action
        current_action_config = self._get_action_config(
            current_action,
            self.action_fields_map
        )

        if current_action_config is None:
            return super().get_field_names(declared_fields, info)
        
        fields = list(current_action_config.get('fields', None))
        fields_to_remove = current_action_config.get('exclude', None)

        if fields_to_remove:
            for field in fields_to_remove:
                fields.remove(field)
        
        return fields

    # Overriding the default get_field method
    def get_fields(self):
        declared_fields = super().get_fields()
        # Checking if the view is passed to the serializer instance
        if not (self.context and self.context.get('view', None)):
            return declared_fields

        if self.action_fields_map is None:
            return declared_fields

        current_action = self.context.get('view').action

        current_action_config = self._get_action_config(
            current_action,
            self.action_fields_map
        )

        if not current_action_config:
            return declared_fields
                
        new_fields = declared_fields.copy()

        custom_fields: dict = current_action_config.get('custom_fields')
        if custom_fields:
            for key, value in custom_fields.items():
                new_fields[key] = value
    
        return new_fields
