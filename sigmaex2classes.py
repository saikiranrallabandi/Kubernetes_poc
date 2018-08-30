import json

import logging
import urllib

import requests
import sys

import docker
from docker import DockerClient, tls, types

import boto3
import ast
import urllib2
from docker.api import APIClient, client
from SigmaTimer import InfiniteTimer

def runBackgroundJobs(func):
    t = InfiniteTimer(0.1, func)
    t.start()

# General utils methods
def make_kv_pair(params):
    x = ' '
    kv_pairs = []
    for k, v in ast.literal_eval(json.dumps(params)).iteritems():
        kv = {
            "{0}".format("ParameterKey"): k,
            "{0}".format("ParameterValue"): v,
        }
        use_previous = False
        if use_previous != None:
            kv['UsePreviousValue'] = use_previous

        kv_pairs.append(kv)
    print kv_pairs
    return kv_pairs

def get_json(url, data_obj=None):
    try:
        url_final = "{0}".format(url)
        if data_obj:
            querystring = urllib.urlencode(data_obj)
            url_final = "{0}?{1}".format(url, querystring)

        get_headers = {'Content-Type': 'application/json'}
        req = urllib2.Request(url_final, headers=get_headers)
        response = urllib2.urlopen(req)
        json_response = response.read()
        #print "Sigma : json_response ", json_response
        return json.loads(json_response)
    except urllib2.HTTPError as e:
        print e
        return None

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

def dictolist(datadict):
    datalist=[]
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

class AWSClient(object):
    def __init__(self,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION_NAME):
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
        self.AWS_REGION_NAME = AWS_REGION_NAME

    def setregion(self,AWS_REGION_NAME):
        self.AWS_REGION_NAME = AWS_REGION_NAME

    def boto3client(self,resource):
        client = None
        client = boto3.client(resource, self.AWS_REGION_NAME, aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)
        if not client:
            raise ValueError('Not able to initialize boto3 client with configuration.')
        else:
            return client

    def describe_stacks(self,stackname):
        client = self.boto3client('cloudformation')
        res = client.describe_stacks(StackName=stackname)
	return res

    def getelb(self,stackname):
        list=[]
        client = self.boto3client('cloudformation')
        response = client.list_stack_resources(StackName=stackname)
        for fetch in response['StackResourceSummaries']:
            if fetch['ResourceType'] in 'AWS::ElasticLoadBalancing::LoadBalancer':
                list.append(fetch['PhysicalResourceId'])
        client = self.boto3client('elb')
        response = client.describe_load_balancers( LoadBalancerNames=list)
        return response['LoadBalancerDescriptions'][0]['DNSName']

    def getmanagerip(self,stackname):
        list = []
        client = self.boto3client('cloudformation')
        response = client.list_stack_resources(StackName=stackname)
        for fetch in response['StackResourceSummaries']:
            if fetch['ResourceType'] in 'AWS::AutoScaling::AutoScalingGroup':
                list.append(fetch['PhysicalResourceId'])
        client1 = self.boto3client('autoscaling')
        response1 = client1.describe_auto_scaling_groups(AutoScalingGroupNames=[list[0]])
        for autoscaling in response1['AutoScalingGroups']:
            for InstanceId in autoscaling['Instances']:
                list.append(InstanceId['InstanceId'])
        client2 = self.boto3client('ec2')
        response2 = client2.describe_instances(InstanceIds=[list[2]])
        for Reservations in response2['Reservations']:
            for Instances in Reservations['Instances']:
                return Instances['PublicIpAddress']

    def getelb(self,stackname):
        list = []
        client = self.boto3client('cloudformation')
        response = client.list_stack_resources(StackName=stackname)
        for fetch in response['StackResourceSummaries']:
            if fetch['ResourceType'] in 'AWS::ElasticLoadBalancing::LoadBalancer':
                list.append(fetch['PhysicalResourceId'])
        client = self.boto3client('elb')
        response = client.describe_load_balancers(LoadBalancerNames=list)
        return response['LoadBalancerDescriptions'][0]['DNSName']

class SwarmClient(object):

    #def __init__(self, dockerhost,username,password,registry):
    def __init__(self, dockerhost):
        self.url='tcp://'+ dockerhost
        self.client=DockerClient(base_url=self.url)
        #self.client.login(username='admin', password='Ayappa2017@', email='sigmaex2@gmail.com', registry='sigmaxm.com')
        #self.client.login(username=username, password=password,email='sigmaex2@gmail.com',registry=registry)

    def reglogin(self, username='admin', password='Ayappa2017@', email='sigmaex2@gmail.com', registry='sigmaxm.com'):
    #def reglogin(self, username, password,registry):
        #res = self.client.login()
        email='sigmaex2@gmail.com'
        res = self.client.login(username=username, password=password,email=email,registry=registry)
        return res

    def managerdetails( self ):
        res = self.client.api.nodes(filters={'role': 'manager'})
        resList=[]
        for r in res:
            _tempdict={}
            _tempdict['managerhostname'] = r['Description']['Hostname']
            _tempdict['managerip'] = r['Status']['Addr']
            _tempdict['engineversion'] = r['Description']['Engine']['EngineVersion']
            _tempdict['managerstatus'] = r['Status']['State']
            _tempdict['availability'] = r['Spec']['Availability']
            _tempdict['state'] = r['Status']['State']
            resList.append(_tempdict)

        return resList
    
    def workerdetails( self ):
        res = self.client.api.nodes(filters={'role': 'worker'})
        resList=[]
        for r in res:
            _tempdict={}
            _tempdict['workerhostname'] = r['Description']['Hostname']
            _tempdict['workerip'] = r['Status']['Addr']
            _tempdict['engineversion'] = r['Description']['Engine']['EngineVersion']
            _tempdict['workerstatus'] = r['Status']['State']
            _tempdict['availability'] = r['Spec']['Availability']
            _tempdict['state'] = r['Status']['State']
            resList.append(_tempdict)
        return resList
    
    def createservice( self, service_name,host_port,container_port,image,replicas=1,command=None):
        #resources = types.Resources(cpu_reservation=1000000000)
        policy = types.RestartPolicy(condition="none")
        replica_mode=types.ServiceMode(mode='replicated',replicas=replicas)
        endpointSpec = docker.types.EndpointSpec(ports={ host_port:container_port })
        #service = self.client.services.create(name=service_name,image=image, command=['sleep', '120'], resources=resources, restart_policy=policy,endpoint_spec=endpointSpec,mode=replica_mode)
        service = self.client.services.create(name=service_name,image=image, restart_policy=policy,endpoint_spec=endpointSpec,mode=replica_mode)
        return service

    def remove_service( self, service_name):
        sn=self.client.services.get(service_name)
        return sn.remove()


class dockerregistry(object):

    def __init__(self, url, username=None,password=None,ssl=False):
        self.url=url
        self.username = username
        self.password = password
        self.ssl = ssl

    def get_reqistry_request(self,regurl):
        req = None
        if self.ssl==True:
            proto="https://"
        else:
            proto="http://"

        url_endpoint = proto + regurl
        s = requests.Session()
        if(self.username!=None):
            s.auth = (self.username, self.password)
        try:
            req = s.get(url_endpoint, verify=False)
        except requests.ConnectionError:
            print 'Cannot connect to Registry'
        return req

    def get_registry_catalog_request(self):
    	requrl = self.url+"/v2/_catalog"
    	req = self.get_reqistry_request(requrl)
    	return req

    def get_registry_tag_request(self,repo):
    	requrl = self.url + "/v2/" + repo  + "/tags/list"
    	req = self.get_reqistry_request(requrl)
    	return req

    def get_all_repos(self):
        req = self.get_registry_catalog_request()
        repo_array = None
        parsed_json = None
        if(req!=None):
                parsed_json = json.loads(req.text)
        if('repositories' in parsed_json):
                repo_array = parsed_json['repositories']
        return repo_array

    def get_tags_for_repo(self, repo):
        repo_tag_url_req = self.get_registry_tag_request(repo)
        parsed_repo_tag_req_resp = json.loads(repo_tag_url_req.text)
        return parsed_repo_tag_req_resp["tags"]

    def get_all_repo_dict(self, repo_array):
        repo_dict = {}
        if (repo_array!=None):
                for repo in repo_array:
                        parsed_repo_tag_req_resp = self.get_tags_for_repo(repo)
                        repo_dict[repo] = parsed_repo_tag_req_resp

        return repo_dict

    def registry_list(self):
        all_repos = self.get_all_repos()
        results = self.get_all_repo_dict(all_repos)
        return results

class StackClient(object):

    def __init__(self,_AWSClient,_StackName ):
        self._AWSClient = _AWSClient
        self._StackName = _StackName

    def setapp(self,app):
        self.app = app

    def createstack(self,payload ):

        kv_pairs = make_kv_pair(payload)

        try:
            template_object = get_json(self.app.config["TEMPLATE_URL"])
            client = self._AWSClient.boto3client('cloudformation')

            response = client.create_stack(
                StackName=self._StackName,
                TemplateBody=json.dumps(template_object),
                Parameters=kv_pairs,
                Capabilities=['CAPABILITY_IAM'],

            )

            if 'ResponseMetadata' in response and \
                            response['ResponseMetadata']['HTTPStatusCode'] < 300:
                logging.info("succeed. response: {0}".format(json.dumps(response)))
            else:
                logging.critical("There was an Unexpected error. response: {0}".format(json.dumps(response)))

        except ValueError as e:
            logging.critical("Value error caught: {0}".format(e))

        return response

    def removestack(self):
        print self._StackName
        client = self._AWSClient.boto3client('cloudformation')
        response = client.delete_stack(StackName=self._StackName );
        return response



