# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,too-few-public-methods,unused-argument
from ..serializers import BaseUserSerializer


class ErrorUserSerializer(BaseUserSerializer):

    default_error_messages = {
        "fail_username_1": "fields(username): case-1",
        "fail_username_2": "fields(username): case-2",
        "fail_password_a": "fields(password): case-a",
        "fail_password_b": "fields(password): case-b",
        "run_bar": "run_validators:bar",
        "run_foo": "run_validators:foo",
        "validate": "validate_failed",
    }


class ValidatorsUserSerializer(ErrorUserSerializer):

    def run_validators(self, value):
        self.validators = [
            self.fail_bar,
            self.fail_foo,
        ]
        return super(ValidatorsUserSerializer, self).run_validators(value)

    def fail_bar(self, value):
        self.fail("run_bar")

    def fail_foo(self, value):
        self.fail("run_foo")


class ValidateUserSerializer(ErrorUserSerializer):

    def validate(self, attrs):
        return self.fail("validate")


class FieldsUserSerializer(ErrorUserSerializer):

    def __init__(self, *args, **kwargs):
        super(FieldsUserSerializer, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(self.fail_username_1)
        self.fields['username'].validators.append(self.fail_username_2)
        self.fields['password'].validators.append(self.fail_password_a)
        self.fields['password'].validators.append(self.fail_password_b)

    def fail_username_1(self, value):
        self.fail("fail_username_1")

    def fail_username_2(self, value):
        self.fail("fail_username_2")

    def fail_password_a(self, value):
        self.fail("fail_password_a")

    def fail_password_b(self, value):
        self.fail("fail_password_b")
