import os

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))
MYSQL_DATABASE_USER = 'root'
#MYSQL_DATABASE_PASSWORD = 'ayappa2017'
MYSQL_DATABASE_DB = 'sigmaex2'
#MYSQL_DATABASE_HOST = 'sigmaex2.cw95aecewzqi.us-west-2.rds.amazonaws.com'
MYSQL_DATABASE_HOST = '127.0.0.1:3306'
DEBUG = True
TEMPLATE_URL = 'https://s3-us-west-2.amazonaws.com/sigmaex2dockertemplate/sigma.tmpl'
#TEMPLATE_URL = 'https://editions-us-east-1.s3.amazonaws.com/aws/stable/Docker.tmpl'
#REGISTRY_URL='sigmaxm.com:5000'
REGISTRY_URL='https://hub.docker.com'
REGISTRY_USERNAME='sigmaex2'
REGISTRY_PASSWORD='Ayappa2017@'
#SQLALCHEMY_DATABASE_URI = 'mysql://sigmaex2:ayappa2017@sigmaex2.cw95aecewzqi.us-west-2.rds.amazonaws.com/sigmaex2'
SQLALCHEMY_DATABASE_URI = 'mysql://root@127.0.0.1:3306/sigmaex2'
SQLALCHEMY_TRACK_MODIFICATIONS=False
TF_WORKING_DIR="/Users/saikiranrallabandi/sigmaxm-tfstate/"
TF_ROOT_EXEC_DIR="/Users/saikiranrallabandi/sigmaex2-gentellella/tf-aws-docker/"
CELERY_BROKER_URL = "redis://admin:ayappa2017@ec2-35-164-18-132.us-west-2.compute.amazonaws.com:6379/0"
CELERY_RESULT_BACKEND = "redis://admin:ayappa2017@ec2-35-164-18-132.us-west-2.compute.amazonaws.com:6379/0"
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.add',
        'schedule': crontab(minute='*/1'),
        'args': (1,2)
    },
}
#/usr/local/bin/celery worker -A sigmaxmApp.celery --loglevel=info --beat
