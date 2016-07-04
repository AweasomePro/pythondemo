from rest_framework import serializers

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self,*args,**kwargs):
        #Don't pass the 'fiels' arg up tp the superclass
        fields = kwargs.pop('fields',None)
        excludes = kwargs.pop('excludes', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args,**kwargs)

        if fields is not None :
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if excludes is not None:
            existing = set(self.fields.keys())
            disallowed = set(excludes)
            for field_name in existing & disallowed:
                self.fields.pop(field_name)