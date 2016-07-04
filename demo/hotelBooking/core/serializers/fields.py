from rest_framework import serializers
from rest_framework.serializers import Field
# class ColorField(serializers.Field):
#     """
#     Color objects are serialized into 'rgb(#, #, #)' notation.
#     """
#     def to_representation(self, obj):
#         return "rgb(%d, %d, %d)" % (obj.red, obj.green, obj.blue)
#
#     def to_internal_value(self, data):
#         data = data.strip('rgb(').rstrip(')')
#         red, green, blue = [int(col) for col in data.split(',')]
#         return Color(red, green, blue)
# class EnumInterFields(serializers.Field):

