import ast
import urllib
import urllib2
import logging
import requests
import yaml
from botocore import regions
from flask import Flask, render_template, url_for, request, json, flash, jsonify
import flask.ext.login
from flask_httpauth import HTTPBasicAuth
from flask import make_response
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, login_manager
from sigmaex2classes import dockerregistry, runBackgroundJobs
from sigmaex2classes import SwarmClient
from werkzeug.utils import redirect
from models import mysql, validate, putawsconfigdata, getawsconfigdata, putregistrydata, getregistrydata, registryhost, \
    putservicedata, getregistrydetails, getservicedata, getdockerswarmdata, getswarmdict, getdashboardData, \
    deleteservicedata, deleteswarmdata, getswarminfo,getmanagerinfo, getmanagerdetailsinfo,getworkerinfo,getworkderdetailsinfo,putswarmdata,getserviceiddata
from sigmaex2classes import sortdictolist
#from utils import runBackgroundJobs, tick, registrylist
from sigmaex2classes import StackClient, AWSClient

instancetype = []

app = Flask(__name__)
app.config.from_object('config')

# Final version we need to create a database object so we don't need to read the app.conf again the models.py
# We need to fix this later after demo
_sessiondata,_sessioncolumns = getawsconfigdata ( )
_awsclient = AWSClient(_sessiondata[0]['AWS_ACCESS_KEY_ID'],_sessiondata[0]['AWS_SECRET_ACCESS_KEY'], _sessiondata[0]['AWS_REGION_NAME'])
app.config.update(_sessiondata[0])
print app.config
# After login we need to make sure app.config.AWSClient context is saved
mysql.init_app(app)

#runBackgroundJobs(dashboardData={'awsaccount': 3, 'dockerswarms': 5, 'containers': 5, 'services': 10})
#runBackgroundJobs(_awsclient.getelb('docker5'))

@app.route('/404')
def pagenotfound():
    render_template('404.html')



@app.errorhandler(404)
def page_not_founds(e):
    return redirect('/404')


# @app.errorhandler(401)
# def page_not_founds(e):
#     return redirect('/maintenance/401')


# Route to any template
@app.route('/',  methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        print username
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))

    accountids=[493665568723]
    return render_template('login.html', error=error,accountids=accountids)

@app.route('/dashboard')
def dashboard():
    SwarmName='docker6'
    SwarmURL=_awsclient.getmanagerip(SwarmName) + ":3000"

    #dashboardData = {'awsaccount': getaccountcount(), 'dockerswarms': 5 'containers': 5, 'services': 10}
    dashboardData = getdashboardData()
    return render_template('dashboard.html',SwarmURL=SwarmURL,dashboardData=dashboardData)

@app.route('/aws',methods=['GET', 'POST'])
def aws():
    datadict, dbcolumns = getawsconfigdata()
    dbdata=sortdictolist(datadict,dbcolumns)
    return render_template('aws_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title='AWS Settings ')

@app.route('/awssettings',methods=['GET', 'POST'])
def awssettings():
    regions = ['ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1',
               'ca-central-1', 'ap-southeast-1', 'ap-south', 'east-2', 'eu-central-1', 'us-east-1', 'us-east-2',
               'us-west-1', 'us-west-2']
    if request.method == 'POST':
        AccessKey = request.form['AccessKey']
        SecretKey = request.form['SecretKey']
        Region = request.form['Region']
        AWSAccountID = request.form['AWSAccountID']
        putawsconfigdata(AccessKey, SecretKey, Region, AWSAccountID)
        return redirect(url_for('aws'))
    return render_template('awssettings.html',names=regions)

@app.route('/registry',methods=['GET', 'POST'])
def registry():
    datadict, dbcolumns = getregistrydata()
    dbdata=sortdictolist(datadict,dbcolumns)
    return render_template('registry_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="Registry Details")

@app.route('/registrysettings',methods=['GET', 'POST'])
def registrysettings():
    if request.method == 'POST':
        Registry = request.form['Registry']
        RegistryUsername = request.form['RegistryUsername']
        RegistryPassword = request.form['RegistryPassword']
        putregistrydata(Registry,  RegistryUsername, RegistryPassword)
        return redirect(url_for('registry'))
    return render_template('registrysettings.html')

@app.route('/listimages',methods=['GET', 'POST'])
def listimages():
    reg = dockerregistry(app.config["REGISTRY_URL"])
    imagedata=reg.registry_list()
    imagedata1 = reg.get_registry_catalog_request()
    print imagedata1
    #print imagedata
    dbcolumns= [
        {
            "field": "tag",
            "title": "tag",
            "sortable": True,
        },
        {
            "field": "image_name",
            "title": "image_name",
            "sortable": True,
        }
    ]
    imagedatalist=[]
    temp={}
    for k,v in imagedata.items():
        #print str(k)
        for lv in v:
            #print " ---" + str(lv)
            temp['image_name']=str(k)
            temp['tag']=str(lv)
            imagedatalist.append(temp)
            temp={}
    dbdata = sortdictolist(imagedatalist,dbcolumns)
    return render_template('image_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title='Images Table')

@app.route('/createservice',methods=['GET', 'POST'])
def createservice():
    host=registryhost()
    print host
    if request.method == 'POST':
        SwarmName=request.form['SwarmName']
        SwarmURL=_awsclient.getmanagerip(request.form['SwarmName']) + ":2375"
        print SwarmURL
        #SwarmURL='54.245.31.33:2375'
        ServiceName = request.form['ServiceName']
        print ServiceName
        ImageName = request.form['ImageName']
        print "ImageName " + ImageName
        HostPort = int(request.form['HostPort'])
        print HostPort
        ContainerPort = int(request.form['ContainerPort'])
        print ContainerPort
        DockerRegistry = request.form['DockerRegistry']
        print DockerRegistry
        Replicas = int(request.form['Replicas'])
        print Replicas
        #Command = request.form['ContainerPort']

        putservicedata(SwarmName,SwarmURL,ServiceName,ImageName,HostPort,ContainerPort,DockerRegistry,Replicas)
        registry_username,registry_password=getregistrydetails(DockerRegistry)
        sc = SwarmClient(dockerhost=SwarmURL)
        sc.reglogin(username=registry_username,password=registry_password,registry=DockerRegistry)
        sc.createservice(service_name=ServiceName,host_port=HostPort,container_port=ContainerPort,image=DockerRegistry+"/"+ImageName,command=None,replicas=Replicas)
        datadict, dbcolumns = getservicedata()
        for index, item in enumerate(datadict):
            datadict[index]['dnsname'] = "http://" + _awsclient.getelb(datadict[index]['SwarmName']) + ":" + str(datadict[index]['HostPort'])
        dbdata=sortdictolist(datadict,dbcolumns)
        print datadict
        return render_template('service_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="Service Details")
    return render_template('createservice.html',names=host)

@app.route('/viewservices',methods=['GET', 'POST'])
def viewservices():
    datadict, dbcolumns = getservicedata()
    #print datadict
    for index, item in enumerate(datadict):
        datadict[index]['dnsname'] = "http://" + _awsclient.getelb(datadict[index]['SwarmName']) + ":" + str(
            datadict[index]['HostPort'])
    dbdata = sortdictolist(datadict, dbcolumns)
    print dbdata
    return render_template('service_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="Service Details")

@app.route('/deleteservice',methods=['POST'])
def deleteservice():
    serviceList = request.get_json()
    print "serviceList"
    print serviceList
    #print type(serviceList)

    # Based on these values we will delete backend database rows..
    for service in serviceList:
        print service
        _tempdict=getserviceiddata(service)
        print "_tempdict"
        print _tempdict
        swarmname=_tempdict[0]['SwarmName']
        print "swarmname"
        print swarmname
        servicename=_tempdict[0]['ServiceName']
        sc = SwarmClient(dockerhost=_awsclient.getmanagerip(swarmname) + ":2375")
        print sc
        sc.remove_service(servicename)
        deleteservicedata(service)

    datadict, dbcolumns = getservicedata()
    #datadict, dbcolumns = getdockerswarmdata()
    dbdata=sortdictolist(datadict,dbcolumns)
    #return render_template('table_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="DockerSwarm Clusters")
    return render_template('service_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="DockerSwarm Clusters")

# PENDING
@app.route('/viewservicedtails')
def viewservicedtails():
    return render_template('viewservicedetails.html')

# -- DockerSwarm block
@app.route('/dockerswarm',methods=['GET', 'POST'])
def dockerswarm():
    datadict, dbcolumns = getdockerswarmdata()
    dbdata=sortdictolist(datadict,dbcolumns)
    return render_template('dockerswarm_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="DockerSwarm Clusters")

@app.route('/createdockerswarm',methods=['GET', 'POST'])
def createdockerswarm():
    KeyNames=['sigmaex2KeyPair']
    if request.method == 'POST':
        SwarmName = request.form['SwarmName']
        KeyName = request.form['KeyName']
        EnableCloudWatchLogs = 'yes'
        EnableSystemPrune = 'no'
        ManagerInstanceType = request.form['ManagerInstanceType']
        ManagerSize = request.form['ManagerSize']
        print "ManagerSize = " + str(ManagerSize)
        ManagerDiskType = request.form['ManagerDiskType']
        ManagerDiskSize = request.form['ManagerDiskSize']
        InstanceType = request.form['InstanceType']
        ClusterSize = request.form['ClusterSize']
        WorkerDiskType = request.form['WorkerDiskType']
        WorkerDiskSize = request.form['WorkerDiskSize']

        payload = {
            #"SwarmName" : str(SwarmName),
            "KeyName" : str(KeyName) ,
            "EnableCloudWatchLogs" : str(EnableCloudWatchLogs),
            "EnableSystemPrune": str(EnableSystemPrune),
            "ManagerInstanceType" :str(ManagerInstanceType),
            "ManagerSize" :str(ManagerSize),
            "ManagerDiskType": str(ManagerDiskType),
            "ManagerDiskSize":str(ManagerDiskSize),
            "InstanceType" :str(InstanceType),
            "ClusterSize" : str(ClusterSize),
            "WorkerDiskType" :str(WorkerDiskType),
            "WorkerDiskSize" :str(WorkerDiskSize),
        }

        sc=StackClient(_awsclient,str(SwarmName))
        sc.setapp(app)
        res1=sc.createstack(payload)
        #res1={u'StackId': 'arn:aws:cloudformation:us-west-2:493665568723:stack/docker8/fa41beb0-eff8-11e7-8d45-503ac9ec2499', 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'fa264798-eff8-11e7-b960-7756fe6df2f7', 'HTTPHeaders': {'x-amzn-requestid': 'fa264798-eff8-11e7-b960-7756fe6df2f7', 'date': 'Tue, 02 Jan 2018 20:10:28 GMT', 'content-length': '377', 'content-type': 'text/xml'}}}
        res2=_awsclient.describe_stacks(stackname=str(SwarmName))
        print "StackClient"
        print res2['Stacks'][0]['StackId']
        print res2['Stacks'][0]['StackName']
        print res2['Stacks'][0]['StackStatus']
        print res2['Stacks'][0]['CreationTime']
        putswarmdata(res2['Stacks'][0]['StackId'], SwarmName, res2['Stacks'][0]['CreationTime'], WorkerDiskSize, EnableCloudWatchLogs, ManagerDiskSize, EnableSystemPrune, ClusterSize, KeyName, ManagerDiskType, ManagerSize, WorkerDiskType, InstanceType, ManagerInstanceType, res2['Stacks'][0]['StackStatus'])
        datadict, dbcolumns = getdockerswarmdata()
        dbdata=sortdictolist(datadict,dbcolumns)
        #return render_template('dockerswarm_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="DockerSwarm Details")
        return redirect(url_for('dockerswarm'))
    return render_template('dockerswarm.html',KeyNames=KeyNames)

@app.route('/swarminfo/<string:swarmname>',methods=['GET'])
def swarminfo(swarmname):
    SwarmName = swarmname
    print "NewChange -> ",SwarmName
    _tempdata, swarmcolumns = getswarminfo(SwarmName)
    swarmdata = sortdictolist(_tempdata, swarmcolumns)
    print "swarmdata"
    print swarmdata

    _tempdata, managercolumns = getmanagerinfo(SwarmName)
    managerdata = sortdictolist(_tempdata, managercolumns)
    print "managerdata"
    print managerdata

    #_tempdata, managerdetailcolumns = getmanagerdetailsinfo(SwarmName)
    #print "managerdetailsdata"
    #print managerdetailsdata

    print "SwarmURL -> managerdet"
    #_tempdata, managerdetailcolumns = getmanagerdetailsinfo(SwarmName)
    _tempdata=SwarmClient(_awsclient.getmanagerip(SwarmName) + ":2375" ).managerdetails()
    print _tempdata
    managerdetailcolumns =    [
        {"field": "managerhostname", "title": "managerhostname", "sortable": True},
        {"field": "managerip", "title": "managerip", "sortable": True},
        {"field": "engineversion", "title": "engineversion", "sortable": True},
        {"field": "managerstatus", "title": "managerstatus", "sortable": True},
        {"field": "availability", "title": "availability", "sortable": True},
        {"field": "state", "title": "state", "sortable": True},
    ]
    managerdetailsdata = sortdictolist(_tempdata, managerdetailcolumns)

    _tempdata, workercolumns = getworkerinfo(SwarmName)
    workerdata = sortdictolist(_tempdata, workercolumns)
    print "workerdata"
    print workerdata

    _tempdata=SwarmClient(_awsclient.getmanagerip(SwarmName) + ":2375" ).workerdetails()
    #_tempdata, workerdetailcolumns = getworkderdetailsinfo(SwarmName)
    workerdetailcolumns = [
        {"field": "workerhostname", "title": "workerhostname", "sortable": True},
        {"field": "workerip", "title": "workerip", "sortable": True},
        {"field": "engineversion", "title": "engineversion", "sortable": True},
        {"field": "workerstatus", "title": "workerstatus", "sortable": True},
        {"field": "availability", "title": "availability", "sortable": True},
        {"field": "state", "title": "state", "sortable": True},
    ]
    workerdetailsdata = sortdictolist(_tempdata, workerdetailcolumns)

    print "workerdetailsdata"
    print workerdetailsdata

    print "This request coming form get", SwarmName

    return render_template('swarminfo_template.html', \
                           swarmdata=swarmdata, swarmcolumns=swarmcolumns, swarmtitle='Swarm info', \
                           managerdata=managerdata, managercolumns=managercolumns, mangertitle='Manager Details', \
                           managerdetailsdata=managerdetailsdata, managerdetailcolumns=managerdetailcolumns, \
                           workerdata=workerdata, workercolumns=workercolumns, workertitle='Worker Details', \
                           workerdetailsdata=workerdetailsdata, workerdetailcolumns=workerdetailcolumns);

@app.route('/deletedockerswarm',methods=['POST'])
def deletedockerswarm():
    #dockerswarmList = request.get_json()
    SwarmNames = request.get_json()
    SwarmName = str(SwarmNames[0])
    print SwarmName
    # Based on these values we will delete backend database rows..
    deleteswarmdata(SwarmName)
    sc = StackClient(_awsclient, str(SwarmName))
    res = sc.removestack()
    print res

    datadict, dbcolumns = getdockerswarmdata()
    dbdata=sortdictolist(datadict,dbcolumns)
    return redirect(url_for('dockerswarm'))
    #return render_template('viewdockerswarm.html',dbdata=dbdata,dbcolumns=dbcolumns,title="DockerSwarm Clusters")


@app.route('/vizualizer',methods=['GET', 'POST'])
def vizualizer():
    SwarmDict = getswarmdict(8080)
    for k, v in SwarmDict.iteritems():
        SwarmDict[k] = "http://" + _awsclient.getelb(k) + ":" + "8080"
        #_t = "http://" + _awsclient.getelb(k) + ":" + "8080"
        #print _t
    #    datadict[index]['dnsname'] = "http://" + _awsclient.getelb(SwarmDict[index]['SwarmName']) + ":" + str(SwarmDict[index]['HostPort'])
    print SwarmDict
    return render_template('vizualizer.html',SwarmDict=SwarmDict)

## Errors
@app.errorhandler(403)
def not_found_error(error):
    return render_template('page_403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('page_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('page_500.html'), 500

@app.route('/table_template',methods=['GET', 'POST'])
def table_template():
    datadict, dbcolumns = getawsconfigdata()
    dbdata=sortdictolist(datadict,dbcolumns)
    return render_template('table_template.html',dbdata=dbdata,dbcolumns=dbcolumns,title="Table Template")

@app.route('/index',  methods=['GET'])
def index():
    return render_template('index.html')

