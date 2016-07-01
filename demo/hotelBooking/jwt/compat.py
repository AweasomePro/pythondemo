from django.contrib.auth import get_user_model

from rest_framework import serializers


class Serializer(serializers.Serializer):
    @property
    def object(self):
        return self.validated_data


class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = {'input_type': 'password'}
        else:
            kwargs['style']['input_type'] = 'password'
        super(PasswordField, self).__init__(*args, **kwargs)


def get_username_field():
    try:
        username_field = get_user_model().USERNAME_FIELD
        print('username_field is '.format(username_field))
    except:
        username_field = 'phone_number'
        print('使用了重载的username_field{}'.format(username_field))
    return username_field


def get_username(user):
    try:
        username = user.phone_number
    except AttributeError:
        username = user.user_name
    print('从用户得 username 得到{}'.format(username))
    return username
