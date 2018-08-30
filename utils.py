#!/usr/local/bin/python3
# coding: utf-8
import logging
import boto3
import requests
from flask.ext.mysql import MySQL
from flask import Flask, abort, request, app
import json

from werkzeug import http

from SigmaTimer import InfiniteTimer

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL()
mysql.init_app(app)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def get_log_level(level_string):
    levels = {
        "DEBUG":logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "CRITICAL":logging.CRITICAL
    }
    return levels[level_string]

# replace all *_client with this common method
def boto3client(resource):
    client = None
    awsconfiglist = []
    awsconfigkey = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION_NAME']
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("select * from awsconfig LIMIT 1")
    auth = cur.fetchall()
    for row in auth:
        aws_access_id = row[1]
        aws_secret_key = row[2]
        aws_region_name = row[3]
        awsconfiglist.append(aws_access_id)
        awsconfiglist.append(aws_secret_key)
        awsconfiglist.append(aws_region_name)
        dictionary = dict(zip(awsconfigkey, awsconfiglist))
    client = boto3.client(resource,
                          dictionary['AWS_REGION_NAME'], aws_access_key_id=dictionary['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=dictionary['AWS_SECRET_ACCESS_KEY'])
    if not client:
        raise ValueError('Not able to initialize boto3 client with configuration.')
    else:
        return client


def make_cloudformation_client():
    client = None
    awsconfiglist = []
    awsconfigkey = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION_NAME']
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("select * from awsconfig")
    auth = cur.fetchall()
    for row in auth:
        aws_access_id = row[1]
        aws_secret_key = row[2]
        aws_region_name = row[3]
        awsconfiglist.append(aws_access_id)
        awsconfiglist.append(aws_secret_key)
        awsconfiglist.append(aws_region_name)
        dictionary = dict(zip(awsconfigkey, awsconfiglist))
    client = boto3.client('cloudformation',
                          dictionary['AWS_REGION_NAME'], aws_access_key_id=dictionary['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=dictionary['AWS_SECRET_ACCESS_KEY'])
    if not client:
        raise ValueError('Not able to initialize boto3 client with configuration.')
    else:
        return client

def make_autoscaling_client():
    client = None
    awsconfiglist = []
    awsconfigkey = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION_NAME']
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("select * from awsconfig")
    auth = cur.fetchall()
    for row in auth:
        aws_access_id = row[1]
        aws_secret_key = row[2]
        aws_region_name = row[3]
        awsconfiglist.append(aws_access_id)
        awsconfiglist.append(aws_secret_key)
        awsconfiglist.append(aws_region_name)
        dictionary = dict(zip(awsconfigkey, awsconfiglist))
    client = boto3.client('autoscaling',
                          dictionary['AWS_REGION_NAME'], aws_access_key_id=dictionary['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=dictionary['AWS_SECRET_ACCESS_KEY'])
    if not client:
        raise ValueError('Not able to initialize boto3 client with configuration.')
    else:
        return client
def make_ec2_client():
    client = None
    awsconfiglist = []
    awsconfigkey = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION_NAME']
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("select * from awsconfig")
    auth = cur.fetchall()
    for row in auth:
        aws_access_id = row[1]
        aws_secret_key = row[2]
        aws_region_name = row[3]
        awsconfiglist.append(aws_access_id)
        awsconfiglist.append(aws_secret_key)
        awsconfiglist.append(aws_region_name)
        dictionary = dict(zip(awsconfigkey, awsconfiglist))
    client = boto3.client('ec2',
                          dictionary['AWS_REGION_NAME'], aws_access_key_id=dictionary['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=dictionary['AWS_SECRET_ACCESS_KEY'])
    if not client:
        raise ValueError('Not able to initialize boto3 client with configuration.')
    else:
        return client
def StackStatus():
    StackStatus = []
    client = make_cloudformation_client()
    response = client.describe_stacks(StackName='dockerswarm4')
    for fecth in response['Stacks']:
        StackStatus.append(fecth['StackStatus'])
    Stack = ''.join(StackStatus)
    return Stack


# sched = BlockingScheduler()
#
# # Schedule job_function to be called every two hours
# sched.add_job(StackStatus, 'interval', minute=5)
#
# sched.start()


def getmanagerip(stackname):
    list = []
    client = make_cloudformation_client()
    response = client.list_stack_resources(StackName=stackname)
    for fetch in response['StackResourceSummaries']:
        if fetch['ResourceType'] in 'AWS::AutoScaling::AutoScalingGroup':
            list.append(fetch['PhysicalResourceId'])
    client1 = make_autoscaling_client()
    response1 = client1.describe_auto_scaling_groups(AutoScalingGroupNames=[list[0]])
    for autoscaling in response1['AutoScalingGroups']:
        for InstanceId in autoscaling['Instances']:
            list.append(InstanceId['InstanceId'])
    client2 = make_ec2_client()
    response2 = client2.describe_instances(InstanceIds=[list[2]])
    for Reservations  in response2['Reservations']:
        for Instances in Reservations['Instances']:
            return Instances['PublicIpAddress']

def getelb(stackname):
    list=[]
    client = boto3client('cloudformation')
    response = client.list_stack_resources(StackName=stackname)
    for fetch in response['StackResourceSummaries']:
        if fetch['ResourceType'] in 'AWS::ElasticLoadBalancing::LoadBalancer':
            list.append(fetch['PhysicalResourceId'])
    client = boto3client('elb')
    response = client.describe_load_balancers( LoadBalancerNames=list)
    return response['LoadBalancerDescriptions'][0]['DNSName']

def tick():
    print s


def runBackgroundJobs():
    t = InfiniteTimer(0.1, tick())
    t.start()

def dictolist(datadict):
    datalist
    templist=[]
    for l in datadict:
        print "SAI1"
        print l
        #print l
        for k,v in l.items():
            print v
            templist.append(str(v))
        datalist.append(templist)
        templist=[]
    return datalist

def sortdictolist(datadict,dbcolumns):
    #print datadict
    #print dbcolumns
    sortedList=[]
    for l in dbcolumns:
        sortedList.append(l['field'])
    #print sortedList
    datalist=[]
    ordered_dict_items=[]
    for l in datadict:
        #print l
        templist=[]
        templist=list(l.get(i) for i in sortedList)
        datalist.append(templist)

    return datalist


def registrylist():
    url = "https://sigmaxm.com/v2/_catalog"

    headers = {
        'authorization': "Basic YWRtaW46QXlhcHBhMjAxN0A=",
        'access-control-allow-credentials': "true",
        'access-control-allow-headers': "Origin, Authorization",
        'access-control-allow-methods': "GET",
        'access-control-allow-origin': "https://sigmaxm.com/v2/_catalog",
        'cache-control': "no-cache",
        'postman-token': "e7278db1-6c04-8c32-5c3e-f6e3d45118cc"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

    return response.text
