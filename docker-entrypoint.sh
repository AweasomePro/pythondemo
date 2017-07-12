touch /tmp/supervisor.sock
chmod 777 /tmp/supervisor.sock
supervisord -c /etc/supervisor/conf.d/supervisor-app.conf
supervisorctl -c /etc/supervisor/conf.d/supervisor-app.conf reload
supervisorctl -c /etc/supervisor/conf.d/supervisor-app.conf start