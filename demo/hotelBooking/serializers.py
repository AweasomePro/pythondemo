from rest_framework import serializers

# username = models.CharField(max_length=50)
# password = models.CharField(max_length=30)
# email = models.EmailField
# phoneNumber = models.IntegerField(max_length=15)
# register_time = models.DateTimeField(auto_created=True)

from .models import  Member,Installation


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self,*args,**kwargs):
        #Don't pass the 'fiels' arg up tp the superclass
        fields = kwargs.pop('fields',None)
        super(DynamicFieldsModelSerializer, self).__init__(*args,**kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('name','email','phoneNumber','registerTime')

class InstallationSerializer(DynamicFieldsModelSerializer):
    # badge = models.BigIntegerField()
    # channels = ListField()
    # deviceProfile = models.CharField(max_length=200)
    # deviceToken = models.CharField(max_length=200, unique=True)
    # deviceType = models.CharField(max_length=200)
    # installationId = models.CharField(max_length=200, unique=True)
    # timeZone = models.CharField(max_length=200)
    class Meta:
        model = Installation
        # choices = {'badge','deviceProfile','installationId','timeZone'}






