# Pull base image
FROM ubuntu:14.04
ADD ./chaolife/requirements.txt /tmp/requirements.txt
RUN apt-get upgrade
RUN apt-get update
RUN apt-get install -y libtiff4-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
RUN apt-get install -y python3-pip
RUN apt-get install -y python-dev
RUN apt-get install -y python3-dev
RUN pip3 install  gunicorn celery
RUN apt-get install -y supervisor nginx 
RUN pip3 install -r /tmp/requirements.txt

# setup all the configfiles
RUN rm -v /etc/nginx/nginx.conf
ADD nginx-app.conf /etc/nginx/nginx.conf
COPY supervisor-app.conf /etc/supervisor/conf.d/

# set env config
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /www
COPY . /www
WORKDIR /www/
#COPY docker-entrypoint.sh docker-entrypoint.sh
#RUN chmod +x docker-entrypoint.sh
EXPOSE 80
EXPOSE 9001
CMD ["supervisord","-n"]
#CMD /www/docker-entrypoint.sh
