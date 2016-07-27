from logging import getLogger
import time
import collections

import django
from django.db import models
from django.db.models import query
try:
    from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor as ForwardManyToOneDescriptor
except ImportError:
    from django.db.models.fields.related_desciptors import ForwardManyToOneDescriptpr

logger = getLogger(__name__)

class PrefetchManagerMixin(models.Manager):
    user_for_related_fields = True
    prefetch_definitions = {}

    @classmethod
    def get_queeryset_class(cls):
        return PrefetchQuerySet



class Prefetcher(object):
    """
    Prefetch definitition .For convenience you can either subclass this and
    define the methods on the subclass or just pass the functions to the contructor.
    Eg, subclassing::
        class GroupPrefetcher(Prefetcher):
            @staticmethod
            def filter(ids):
                return User.groups.through.objects.filter(user__in=ids).select_related('group')
            @staticmethod
            def reverse_mapper(user_group_association):
                return [user_group_association.user_id]
            @staticmethod
            def decorator(user, user_group_associations=()):
                setattr(user, 'prefetched_groups', [i.group for i in user_group_associations])
    Or with contructor::
        Prefetcher(
            filter = lambda ids: User.groups.through.objects.filter(user__in=ids).select_related('group'),
            reverse_mapper = lambda user_group_association: [user_group_association.user_id],
            decorator = lambda user, user_group_associations=(): setattr(user, 'prefetched_groups', [
                i.group for i in user_group_associations
            ])
        )
    Glossary:
    * filter(list_of_ids):
        A function that returns a queryset containing all the related data for a given list of keys.
        Takes a list of ids as argument.
    * reverse_mapper(related_object):
        A function that takes the related object as argument and returns a list
        of keys that maps that related object to the objects in the queryset.
    * mapper(object):
        Optional (defaults to ``lambda obj: obj.id``).
        A function that returns the key for a given object in your query set.
    * decorator(object, list_of_related_objects):
        A function that will save the related data on each of your objects in
        your queryset. Takes the object and a list of related objects as
        arguments. Note that you should not override existing attributes on the
        model instance here.
    """
    collect = False

