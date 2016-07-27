apt-get update
apt-get install python-pip  python-dev python3-dev Nginx
pip install virtualenv virtualenvwrapper
virtualenv -p //python3.4  dir

celery -A HotelBookingProject worker -l info