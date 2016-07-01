from django.db import models
import ast
class ListField(models.TextField):
    """
    user like
    >>> a = Article()
    >>> a.labels.append('Django')
    >>> a.labels.append('custom fields')
    >>> a.labels
    ['Django', 'custom fields']

    >>> type(a.labels)
    <type 'list'>

    >>> a.content = u'我正在写一篇关于自定义Django Fields的教程'
    >>> a.save()
    """
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value,list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class ListModel(models.Model):
    class Meta:
        app_label = 'hotelBooking'
    test_list = ListField()