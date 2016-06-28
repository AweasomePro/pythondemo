import ps, re
from datetime import datetime

#导入Pabric API
from fabric.api import *

# 服务器登入用户名
env.user = 'root'
env.sudo_user = 'root'
env.hosts = ['114.55.144.169']

_TAR_FILE = 'dist-awesome.tar.gz'

def build():
	inclueds = ['demo',]
	excludes = ['.*','*.pyc','*pyo']
	local('rm -f dist/%s'% _TAR_FILE)
	with lcd(os.path.join(os.path.abspath('.'), 'www')):
		cmd = ['tar','--dereference','-czvf','../dist/%s'%_TAR_FILE]
		cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
	    cmd.extend(includes)
	    local(' '.join(cmd))