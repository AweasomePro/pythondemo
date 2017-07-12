'''
Created by auto_sdk on 2016.05.24
'''
from top.api.base import RestApi

"""
阿里短信发送的请求接口
"""
class SetDefaultAppMixin(object):
	def __init__(self,**kwargs):
		from top import getDefaultAppInfo
		self.set_app_info(getDefaultAppInfo())
		super.__init__(kwargs)

class AlibabaAliqinFcSmsNumSendRequest(SetDefaultAppMixin,RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.extend = None
		self.rec_num = None
		self.sms_free_sign_name = None
		self.sms_param = None
		self.sms_template_code = None
		self.sms_type = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.sms.num.send'
