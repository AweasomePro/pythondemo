import re
class IganoreCrsMiddleware(object):
    def process_request(self,request,**karg):
        if re.match(r'^/image/imageUp/?$', request.path):
            request.csrf_processing_done = True
            return None