from django.contrib.auth import authenticate,get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from authtoken.models import Token

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


class VerifyTokenSerializer(serializers.Serializer):
    """
    Check the veracity of an access token.
    """
    token = serializers.CharField()
    phone_number = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        token = attrs['token']
        phone_number = attrs['phone_number']
        token = self._check_token(token=token)
        user = self._check_user(token,phone_number)

        return {
            'token': token,
            'phone_number': user.phone_number
        }

    def _check_token(self, token,):
        try:
            token = Token.objects.get(key=token)
            return token
        except Token.DoesNotExist:
            msg = _('invalidate Token(Doestn\'t exit).')
            raise serializers.ValidationError(msg)

    def _check_user(self,token_obj,phone_number):
        if (token_obj.user.phone_number != phone_number):
            msg = _('invalidate Token .')
            raise serializers.ValidationError(msg)
        return token_obj.user

    @property
    def username_field(self):
        return get_username_field()


def get_username_field():
    try:
        username_field = get_user_model().USERNAME_FIELD
    except:
        username_field = 'username'
    return username_field