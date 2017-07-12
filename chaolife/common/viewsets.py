from dynamic_rest.viewsets import DynamicModelViewSet,WithDynamicViewSetMixin

from chaolife.pagination import StandardResultsSetPagination
from common.utils.AppJsonResponse import DefaultJsonResponse
from authtoken.authentication import TokenAuthentication
from rest_framework.viewsets import  ReadOnlyModelViewSet
class CustomSupportMixin(object):

    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DefaultJsonResponse(serializer.data)

    def initialize_request(self, request, *args, **kargs):
        request = super(CustomSupportMixin,self).initialize_request(request,*args,**kargs)
        return self.supportOrQuery(request)

    def supportOrQuery(self,request):
        print(request.GET)
        query_params = request.GET
        self.splitOrQuery(query_params,['include[]','exclude[]'])
        # includes = query_params.getlist('include[]',None)
        # excludes = query_params.getlist('exclude[]',None)
        # for fields in (includes,excludes):
        #     print('待切割的是{}'.format(fields))
        #     for field in fields:
        #         print('    '.format(field))
        #         print(type(field))
        #         print(field)
        #         split_fields = field.split('|')
        #         if len(split_fields)>1:
        #             fields.remove(field)
        #             query_params.append('include[]',split_fields)
        #         print(field.split('|'))
        #     # print(includes)
        #     # print(excludes)
        return request

    def splitOrQuery(self,queryPrams,supportKeys):
        for queryKey in supportKeys:
            if queryPrams.getlist(queryKey):
                fields = queryPrams.getlist(queryKey)
                for field in fields:
                    print('    '.format(field))
                    print(type(field))
                    print(field)
                    split_fields = field.split('|')
                    if len(split_fields) > 1:
                        fields.remove(field)
                        queryPrams.add(queryKey, split_fields)
                    print(field.split('|'))


class CustomDynamicModelViewSet(CustomSupportMixin,DynamicModelViewSet):
    """
      Create a model instance.
      """


class CustomDynamicReadOnlyModelViewSet(CustomSupportMixin, WithDynamicViewSetMixin, ReadOnlyModelViewSet):
    pass




