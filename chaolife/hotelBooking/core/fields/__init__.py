from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import BLANK_CHOICE_DASH
from django.forms.widgets import NumberInput
from django.utils.translation import ugettext_lazy as _

IdentifierValidator = RegexValidator("[a-z][a-z_]+")

class InternalIdentifierField(models.CharField):
    def __init__(self, **kwargs):
        if "unique" not in kwargs:
            raise ValueError("You must explicitly set the `unique` flag for `InternalIdentifierField`s.")
        kwargs.setdefault("max_length", 64)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", bool(kwargs.get("blank")))  # If it's allowed to be blank, it should be null
        kwargs.setdefault("verbose_name", _("internal identifier"))
        kwargs.setdefault("help_text", _(u"Do not change this value if you are not sure what you're doing."))
        kwargs.setdefault("editable", False)
        super(InternalIdentifierField, self).__init__(**kwargs)
        self.validators.append(IdentifierValidator)

    def get_prep_value(self, value):
        # Save 'None's instead of falsy values (such as empty strings)
        # for 'InternalIdentifierFields' to avoid 'IntegrityError's on unique fields
        prepared_value = super(InternalIdentifierField,self).get_prep_value(value)
        if self.null:
            return (prepared_value or None)
        return prepared_value

    def deconstruct(self):
        (name, path, args, kwargs) = super(InternalIdentifierField, self).deconstruct()
        kwargs["null"] = self.null
        kwargs["unique"] = self.unique
        kwargs["blank"] = self.blank
        # Irrelevant for migrations, and usually translated anyway:
        kwargs.pop("verbose_name", None)
        kwargs.pop("help_text", None)
        return (name, path, args, kwargs)
