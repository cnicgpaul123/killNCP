# -*- coding: utf-8 -*-
""" 用户帐号相关 """
# pylint: disable=too-few-public-methods,abstract-method
from django.utils.translation import gettext_lazy as _
from django.contrib import auth
from rest_framework import serializers
from rest_framework import validators
from applus.django import dao

# pylint: disable=invalid-name
user_dao = dao.get_lazy_dao(None)


class BaseUserSerializer(serializers.ModelSerializer):
    """ 帐号信息 """

    # pylint: disable=missing-docstring
    class Meta:
        model = dao.get_lazy_model(None)
        fields = ['username']


class LoginUserSerializer(BaseUserSerializer):
    """ 登入提交信息 """

    default_error_messages = {
        'invalid_username': "帐号/密码不正确。",
        'invalid_password': "帐号/密码不正确。",
    }

    # pylint: disable=missing-docstring
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['password']

    def __init__(self, *args, **kwargs):
        super(LoginUserSerializer, self).__init__(*args, **kwargs)
        self._user = None
        # 默认会验证 Unique
        for _, field in self.fields.items():
            field.validators = [
                validator
                for validator in field.validators
                if not isinstance(validator, validators.UniqueValidator)
            ]

    def get_validators(self):
        """ 默认会验证 unique_together """
        return []

    def validate_username(self, value):
        """ Validate given username. """
        try:
            self._user = user_dao.get(username=value)
        except user_dao.model.DoesNotExist:
            self.fail('invalid_username')
        return value

    def validate_password(self, value):
        """ Validate given password. """
        if hasattr(self, '_user') and not self._user.check_password(value):
            self.fail('invalid_password')
        return value

    def validate(self, attrs):
        """ Validate given credentials. """
        self.instance = auth.authenticate(**attrs)
        return attrs


class ProfileUserSerializer(BaseUserSerializer):
    """ 登入帐号的信息 """

    # pylint: disable=missing-docstring
    class Meta(BaseUserSerializer.Meta):
        fields = ['username']


class TokenSerializer(serializers.ModelSerializer):
    """ 登入帐号的令牌 """

    # pylint: disable=missing-docstring
    class Meta:
        model = dao.get_lazy_model("authtoken.token")
        fields = ["key"]


class UserForAdminSerializer(BaseUserSerializer):
    """ 管理员可查看的帐号信息 """

    # pylint: disable=missing-docstring
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined']


class PasswordResetSerializer(serializers.Serializer):
    """ 设置密码 """

    default_error_messages = {
        'username_exists': _("A user with that username already exists."),
    }

    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        """ 密码是否安全 """
        auth.password_validation.validate_password(value, self.instance)
        return value

    def update(self, instance, validated_data):
        """ 更新 """
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class PasswordChangeSerializer(PasswordResetSerializer):
    """ 更换密码 """

    default_error_messages = {
        'password_incorrect': _(
            "Your old password was entered incorrectly. Please enter it again."),
    }

    old_password = serializers.CharField()

    def validate_old_password(self, value):
        """ 检查旧密码 """
        if not self.instance.check_password(value):
            self.fail('password_incorrect')
        return value


class CreateUserSerializer(PasswordResetSerializer):
    """ 检查帐号 """

    username = serializers.CharField()

    def validate_username(self, value):
        """ 检查帐号是否存在 """
        try:
            user_dao.get(username=value)
        except user_dao.model.DoesNotExist:
            pass
        else:
            self.fail('username_exists')
        return value

    def init_user(self):
        """ 创建实例(不提交) """
        return user_dao.model(username=self.validated_data['username'])

    def save(self, **kwargs):
        """ 创建 """
        user = self.init_user()
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class CreateStaffSerializer(CreateUserSerializer):
    """ 创建管理员帐号 """

    def init_user(self):
        """ 创建实例，并设置为管理员 """
        user = super(CreateStaffSerializer, self).init_user()
        user.is_staff = True
        return user
