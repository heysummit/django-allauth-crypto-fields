# Courtesy of django-social-auth
import json

from django.core.exceptions import ValidationError
from django.db import models


class JSONField(models.TextField):
    """Simple JSON field that stores python structures as JSON strings
    on database.
    """

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if self.blank and not value:
            return None
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception as e:
                raise ValidationError(str(e))
        else:
            return value

    def validate(self, value, model_instance):
        """Check value is a valid JSON string, raise ValidationError on
        error."""
        if isinstance(value, str):
            super(JSONField, self).validate(value, model_instance)
            try:
                json.loads(value)
            except Exception as e:
                raise ValidationError(str(e))

    def get_prep_value(self, value):
        """Convert value to JSON string before save"""
        try:
            return json.dumps(value)
        except Exception as e:
            raise ValidationError(str(e))

    def value_from_object(self, obj):
        """Return value dumped to string."""
        val = super(JSONField, self).value_from_object(obj)
        return self.get_prep_value(val)


class JSONWrappedTextField(models.TextField):
    """
    A field that will ensure the data entered into it is valid JSON.
    """
    def to_python(self, value):
        if isinstance(value, str):
            value = super(JSONWrappedTextField, self).to_python(value)
            value = json.loads(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super(JSONWrappedTextField, self).get_db_prep_value(value, connection, prepared)
        if isinstance(value, dict):
            value = json.dumps(value)
        return value
