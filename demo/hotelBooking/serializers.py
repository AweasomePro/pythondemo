from rest_framework import serializers

# username = models.CharField(max_length=50)
# password = models.CharField(max_length=30)
# email = models.EmailField
# phoneNumber = models.IntegerField(max_length=15)
# register_time = models.DateTimeField(auto_created=True)

from .models import  Member


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return Member.objects.create(**validated_data)

    def update(self,instance,validated_data):
        # instance.title = validated_data.get('title', instance.title)
        # instance.code = validated_data.get('code', instance.code)
        # instance.linenos = validated_data.get('linenos', instance.linenos)
        # instance.language = validated_data.get('language', instance.language)
        # instance.style = validated_data.get('style', instance.style)
        # instance.save()
        return instance

    class Meta:
        model = Member
        fields = ('name','email','phoneNumber','registerTime')


