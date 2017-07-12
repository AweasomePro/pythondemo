#-*- coding: utf-8 -*-
from functools import wraps

import time
import logging
LOGGER = logging.getLogger(__name__)

def fn_time(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        start_time = time.time
        result = function(*args,**kwargs)
        end_time = time.time()
        print('Total time running %s: %s seconds'.format(function.func_name,str(end_time-start_time)))
        LOGGER.info('Total time running %s: %s seconds'.format(function.func_name,str(end_time-start_time)))
        return result
    return function_timer