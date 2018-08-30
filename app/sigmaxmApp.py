import os
import random

import time
import urllib2

import requests
from celery.schedules import crontab
from flask import Flask, render_template, url_for, request, json, flash, jsonify,session,current_app
import uuid
from bcrypt import hashpw, gensalt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from urllib3 import response

from sigmaxmmodels import User, AWSConfig, Registry, Swarm, Manager_Details, Worker_Details, to_list_of_json, Service, \
    Registry_User, RigisterUser
from sigmaxmclasses import dockerregistry, SigmaxmTerraform, setdirTerraform, createTerraform, \
    destroyTerraform, setsessTerraform, SwarmClient, tf_output
from sigmaxmclasses import sortdictolist,runBackgroundJobs
from sigmaxmclasses import AWSClient
from werkzeug.utils import redirect
from database import db
from sqlalchemy import exc
from celery import Celery
from celery.task import periodic_task


app = Flask(__name__)

app.config.from_object('config')
app.secret_key = os.urandom(24)
app.config.from_envvar("SIGMAXM_ENV",silent=True)


db.app = app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
_awsclient=type('AWSClient', (object,), {})()

# # Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)



USERNAME = {}

# @celery.task(bind=True)
# def long_task(self):
#     """Background task that runs a long function with progress reports."""
#     verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
#     adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
#     noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
#     message = ''
#     total = random.randint(10, 50)
#     for i in range(total):
#         if not message or random.random() < 0.25:
#             message = '{0} {1} {2}...'.format(random.choice(verb),
#                                               random.choice(adjective),
#                                               random.choice(noun))
#         self.update_state(state='PROGRESS',
#                           meta={'current': i, 'total': total,
#                                 'status': message})
#         time.sleep(1)
#     return {'current': 100, 'total': 100, 'status': 'Task completed!',
#             'result': 42}


# @app.route('/404')
# def pagenotfound():
#     render_template('404.html')



@app.errorhandler(404)
def page_not_founds(e):
    return render_template('404.html')

@app.errorhandler(401)
def page_not_founds(e):
    return render_template('401.html')


@app.route('/celery', methods=['GET', 'POST'])
def celery():
    return render_template('celery.html')



@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)



# @celery.task
# def add(x, y):
#     return x + y
# result = add.delay(10,20)
# print result

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))



@app.route('/',methods=['GET', 'POST'])
def sigmaxm():
    email = 'sigmaxm2017@gmail.com'
    password = 'Ayappa2017'
    registered_user = User.query.filter_by(USERNAME=email).first()
    login_user(registered_user)
    session['user_id'] = registered_user.get_id()

    return render_template('index.html')

@app.route('/sigmaxm',methods=['GET', 'POST'])
def sigmaxmhome():
    return render_template('viewdockerswarm_template.html')

@app.route('/index2',methods=['GET', 'POST'])
def index2():
    return render_template('index2.html')



@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = str(uuid.uuid4())
        new_user = User(id=id,
                        USERNAME=request.form['email'],
                        PASSWORD = hashpw(request.form['password'].encode('utf-8'), gensalt(13)))
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.SQLAlchemyError:
            return render_template('page_500.html')
        login_user(new_user)
        session['user_id'] = new_user.get_id()
        print new_user
        return redirect('viewdockerswarm')

    else:
        return render_template('register.html')




@app.route('/home',  methods=['GET'])
@app.route('/index',  methods=['GET'])
@app.route('/index.html',  methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        registered_user = User.query.filter_by(USERNAME=email).first()
        username = User.query.filter_by(id=registered_user.get_id()).first()

        if registered_user is None:
            print('Username is invalid', 'error')
            return redirect('login')

        if not registered_user.check_password(password):
            print('Password is invalid', 'error')
            return redirect('login')

        login_user(registered_user)
        #print 'registered_user.get_id()'
        #print registered_user.get_id()
        session['user_id'] = registered_user.get_id()
        session['username'] = username.USERNAME

        return redirect('viewdockerswarm')
        #return redirect(request.args.get('next') or 'home')
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route('/dashboard')
@login_required
def dashboard():
   swarm_name = 'docker5'
   swarm = db.session.query(Swarm).filter_by(SWARM_NAME=swarm_name).first()
   session['swarm_id'] = swarm.SWARM_ID
   swarm_port = 3000
   setsessTerraform(session, app.config)
   swarm_url = "http://" + tf_output(session, 'master_public_ips')[0] + ":" + str(swarm_port)
   swarm_dict = {}
   swarm_dict[swarm_name] = swarm_url

   return render_template('dashboard.html',swarm_dict=swarm_dict)

@app.route('/api/dashboard')
def api_dashboard():
   dashboardData = {'awsaccount': 1, 'dockerswarms': 5, 'containers': 5, 'services': 10}
   return jsonify(dashboardData)

@app.route('/vizualizer',methods=['GET', 'POST'])
@login_required
def vizualizer():
    swarm_name='docker5'
    swarm = db.session.query(Swarm).filter_by(SWARM_NAME=swarm_name).first()
    print swarm.SWARM_ID
    session['swarm_id'] = swarm.SWARM_ID
    swarm_port = 8080
    setsessTerraform(session, app.config)
    print session
    print tf_output(session, 'master_public_ips')[0]
    viz_url = "http://" + tf_output(session, 'master_public_ips')[0] + ":" + str(swarm_port)
    swarm_dict={}
    swarm_dict[swarm_name] = viz_url
    print swarm_dict

    return render_template('vizualizer.html',SwarmDict=swarm_dict)

@app.route('/aws',methods=['GET'])
@login_required
def aws():
    return render_template('aws_template.html')

@app.route('/api/aws',methods=['GET'])
@login_required
def api_aws():
    _data={'objects':to_list_of_json(AWSConfig.query.all(), AWSConfig)}
    return jsonify(_data)

@app.route('/createaws',methods=['GET', 'POST'])
@login_required
def createaws():
    regions = ['ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1',
               'ca-central-1', 'ap-southeast-1', 'ap-south', 'east-2', 'eu-central-1', 'us-east-1', 'us-east-2',
               'us-west-1', 'us-west-2']
    if request.method == 'POST':
        payload= { "AWSCONFIG_ID" : str(uuid.uuid4()),
                     "AWS_ACCESS_KEY_ID" : request.form['AccessKey'],
                     "AWS_SECRET_ACCESS_KEY" : hashpw(request.form['SecretKey'].encode('utf-8'), gensalt(13)),
                     "AWS_REGION_NAME" : request.form['Region'],
                     "AWS_ACCOUNT_ID" : request.form['AWSAccountID'],
                     "USER_ID" : session['user_id'],
        }

        new_aws = AWSConfig(**payload)
        #print new_aws
        try:
            db.session.add(new_aws)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            print str(err)
            return render_template('page_500.html')
        return redirect(url_for('aws'))
    return render_template('createaws.html',names=regions)

@app.route('/deleteaws', methods=['POST'])
@login_required
def deleteaws():
   awsconfig_id = request.get_json()
   #print "awsconfig_id = " + awsconfig_id
   try:
       AWSConfig.query.filter_by(AWSCONFIG_ID=awsconfig_id).delete()
       db.session.commit()
   except exc.SQLAlchemyError:
       return render_template('page_500.html')

   return "{\"msg\":\"success\"}"

@app.route('/registry',methods=['GET'])
@login_required
def registry():
    return render_template('registry_template.html')

@app.route('/api/viewregistry',methods=['GET'])
@login_required
def api_viewregistry():
    _data={'objects':to_list_of_json(Registry.query.all(), Registry)}
    return jsonify(_data)

@app.route('/registrysettings',methods=['GET', 'POST'])
@login_required
def registrysettings():
    if request.method == 'POST':
        _a = Registry(REGISTRY_ID=str(uuid.uuid4()),
                      REGISTRY_URL=request.form['Registry'],
                      REGISTRY_PORT=5000,
                      REGISTRY_USERNAME=request.form['RegistryUsername'],
                      REGISTRY_PASSWORD=hashpw(request.form['RegistryPassword'].encode('utf-8'), gensalt(13)))

        try:
            db.session.add(_a)
            db.session.commit()
        except exc.SQLAlchemyError:
            return render_template('page_500.html')

        return redirect(url_for('registry'))
    return render_template('registrysettings.html')

@app.route('/deleteregistry', methods=['POST'])
@login_required
def deleteregistry():
   registry_id = request.get_json()
   print registry_id
   try:
       Registry.query.filter_by(REGISTRY_ID=registry_id).delete()
       db.session.commit()
   except exc.SQLAlchemyError:
       return render_template('page_500.html')

   return "{\"msg\":\"success\"}"

@app.route('/listimages',methods=['GET', 'POST'])
#@login_required
def listimages():
    list_images = []
    list_namespace = []
    url = "https://docker.apple.com/v2/_catalog"

    headers = {
        'authorization': "Basic c19yYWxsYWJhbmRpOk1hbWF5YTkyNDcyQA==",
        'cache-control': "no-cache",
        'postman-token': "315d8bc9-002e-8b57-6585-2425e6bf092b"
    }

    request = urllib2.Request(url, headers=headers)

    u = urllib2.urlopen(request)
    json_obj = json.load(u)
    for i in json_obj['repositories']:
        s = "docker.apple.com/" + i

        list_images.append(s)
        #if 's_rallabandi' in i:
            #list_images.append(i.split("/")[-1])

    return render_template('image_template.html',list_images=list_images,list_namespace=list_namespace)

@app.route('/registrylogin',methods=['GET', 'POST'])
#@login_required
def registrylogin():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        registered_user = RigisterUser.query.filter_by(USERNAME=email).first()
        username = User.query.filter_by(id=registered_user.get_id()).first()

        if registered_user is None:
            print('Username is invalid', 'error')
            return redirect('login')

        if not registered_user.check_password(password):
            print('Password is invalid', 'error')
            return redirect('login')

        login_user(registered_user)
        #print 'registered_user.get_id()'
        #print registered_user.get_id()
        session['user_id'] = registered_user.get_id()
        session['username'] = username.USERNAME



        return redirect('listimages')
        #return redirect(request.args.get('next') or 'home')
    else:
        return render_template('registrylogin.html')


@app.route('/test',methods=['GET'])
def test():
    return render_template('test.html')




@app.route('/api/viewimages',methods=['GET'])
#@login_required
def api_viewimages():
    list_images = []

    url = "https://docker.apple.com/v2/_catalog"

    headers = {
        'authorization': "Basic c19yYWxsYWJhbmRpOk1hbWF5YTkyNDcyQA==",
        'cache-control': "no-cache",
        'postman-token': "315d8bc9-002e-8b57-6585-2425e6bf092b"
    }

    request = urllib2.Request(url, headers=headers)

    u = urllib2.urlopen(request)
    json_obj = json.load(u)
    for i in json_obj['repositories']:
        s = 'docker.apple.com/' + i
        list_images.append(s)
    print list_images

    return jsonify(list_images)






# @app.route('/api/viewimages',methods=['GET'])
# #@login_required
# def api_viewimages():
#    reg = dockerregistry(app.config["REGISTRY_URL"])
#    print "sasas",reg.get_registry_catalog_request()
#    imagedata = reg.registry_list()
#    print imagedata
#    imagedatalist = []
#    temp = {}
#    for k, v in imagedata.items():
#        # print str(k)
#        for lv in v:
#            # print " ---" + str(lv)
#            temp['image_name'] = str(k)
#            temp['tag'] = str(lv)
#            imagedatalist.append(temp)
#            temp = {}
#
#    _data={'objects':imagedatalist}
#    return jsonify(_data)

@app.route('/viewdockerswarm',methods=['GET'])
@login_required
def viewdockerswarm():
    return render_template('viewdockerswarm_template.html',)

@app.route('/api/viewdockerswarm',methods=['GET'])
#@login_required
def api_viewdockerswarm():
    _data={'objects':to_list_of_json(Swarm.query.all(), Swarm)}
    return jsonify(_data)

@app.route('/deletedockerswarm', methods=['POST'])
@login_required
def deletedockerswarm():
   swarm_id = request.get_json()
   print swarm_id
   try:
       Swarm.query.filter_by(SWARM_ID=swarm_id).delete()
       db.session.commit()
   except exc.SQLAlchemyError:
       return render_template('page_500.html')

   return "{\"msg\":\"success\"}"

@app.route('/createdockerswarm',methods=['GET', 'POST'])
@login_required
def createdockerswarm():
    KeyNames=['sigmaex2KeyPair']
    if request.method == 'POST':
        swarm_id = str(uuid.uuid4())
        session['swarm_id'] = swarm_id
        session['tworking_dir'] = app.config["TF_WORKING_DIR"] + "/." + session['user_id'] + ":" + session['swarm_id']
        print session['tworking_dir']

        payload = {
            "SWARM_ID" : swarm_id,
            "SWARM_NAME" : str(request.form['SwarmName']),
            "SWARM_STATUS" : "Creation in Progress",
            #"KEYNAME" : str(request.form['KeyName']) ,
            "ENABLECLOUDWATCHLOGS" : str('yes'),
            "ENABLESYSTEMPRUNE": str('no'),
            #Manager
            "MANAGERINSTANCETYPE" :str(request.form['ManagerInstanceType']),
            "MANAGERSIZE" :str(request.form['ManagerSize']),
            "MANAGERDISKTYPE": str(request.form['ManagerDiskType']),
            "MANAGERDISKSIZE":str(request.form['ManagerDiskSize']),
            #Workder
            "INSTANCETYPE" :str(request.form['InstanceType']),
            "CLUSTERSIZE" : str(request.form['ClusterSize']),
            "WORKERDISKTYPE" :str(request.form['WorkerDiskType']),
            "WORKERDISKSIZE" :str(request.form['WorkerDiskSize']),
        }
        new_swarm = Swarm(**payload)
        print new_swarm

        try:
            setsessTerraform(session,app.config)
            setdirTerraform(session,app.config)
            print session
            createTerraform(current_app._get_current_object() ,session, payload)

            db.session.add(new_swarm)
            db.session.commit()
        except exc.SQLAlchemyError:
            return render_template('page_500.html')

        return redirect(url_for('viewdockerswarm'))
    return render_template('dockerswarm.html',KeyNames=KeyNames)

@app.route('/swarminfo/<string:swarm_id>',methods=['GET'])
@login_required
def swarminfo(swarm_id):
    return render_template('swarminfo.html')

@app.route('/api/swarminfo/<string:swarm_id>',methods=['GET'])
@login_required
def api_swarminfo_det(swarm_id):
   _data={'objects':to_list_of_json(Swarm.query.filter(Swarm.SWARM_ID == swarm_id ), Swarm)}
   return jsonify(_data)

@app.route('/api/managerinfo/<string:swarm_id>',methods=['GET'])
@login_required
def api_managerinfo(swarm_id):
   _data={'objects':to_list_of_json(Manager_Details.query.filter(Manager_Details.SWARM_ID == swarm_id ), Manager_Details)}
   print _data
   return jsonify(_data)

@app.route('/api/workerinfo/<string:swarm_id>',methods=['GET'])
@login_required
def api_workerinfo(swarm_id):
   _data={'objects':to_list_of_json(Worker_Details.query.filter(Worker_Details.SWARM_ID == swarm_id ), Worker_Details)}
   return jsonify(_data)

@app.route('/viewservice',methods=['GET'])
@login_required
def viewservice():
    return render_template('viewservice_template.html')

@app.route('/api/serviceinfo',methods=['GET'])
@login_required
def api_serviceinfo():
    _data={'objects':to_list_of_json(Service.query.all(), Service)}
    return jsonify(_data)

@app.route('/deleteservice', methods=['POST'])
@login_required
def deleteservice():
    service_id = request.get_json()
    print service_id
    try:
        Service.query.filter_by(SERVICE_ID=service_id).delete()
        db.session.commit()
    except exc.SQLAlchemyError:
        return render_template('page_500.html')

    return "{\"msg\":\"success\"}"

@app.route('/createservice',methods=['GET', 'POST'])
@login_required
def createservice():
    registry = db.session.query(Registry).first()
    #registry = db.session.query(Registry).join(Registry_User, Registry_User.REGISTRY_ID == Registry.REGISTRY_ID).first()
    print registry
    registry_url = registry.REGISTRY_URL
    print "registry_url = ",registry_url
    #host=['dockerregistry']

    if request.method == 'POST':
        registry = db.session.query(Registry).first()
        registry_url = registry.REGISTRY_URL
        print "s", registry_url

        #SwarmName = request.form['SwarmName']

        swarm = db.session.query(Swarm).filter_by(SWARM_NAME=str(request.form['SwarmName'])).first()
        print swarm.SWARM_ID
        session['swarm_id'] = swarm.SWARM_ID
        swarm_port=2375
        setsessTerraform(session, app.config)
        SwarmURL = tf_output(session,'master_public_ips')[0]+":"+str(swarm_port)
        print "SwarmURL" + SwarmURL
        #SwarmURL = "34.230.71.12:2375"

        SERVICE_NAME = str(request.form['ServiceName'])
        REPLICAS = int(request.form['Replicas'])
        IMAGENAME = str(request.form['ImageName'])
        HOSTPORT = int(request.form['HostPort'])
        CONTAINERPORT = int(request.form['ContainerPort'])
        DockerRegistry = str(request.form['DockerRegistry'])

        #registry = db.session.query(Registry).join(Registry_User, Registry_User.REGISTRY_ID == Registry.REGISTRY_ID).first()
        registry = db.session.query(Registry).first()
        registry_username = registry.REGISTRY_USERNAME
        registry_password = registry.REGISTRY_PASSWORD

        #print register_password
        sc = SwarmClient(dockerhost=SwarmURL)
        sc.reglogin(username=registry_username, password=registry_password,
                    registry=DockerRegistry)
        sc.createservice(service_name=SERVICE_NAME, host_port=HOSTPORT,
                         container_port=CONTAINERPORT,
                         image=DockerRegistry + "/" + IMAGENAME,
                         command=None, replicas=REPLICAS)

        payload = {
            "SERVICE_ID" : str(uuid.uuid4()),
            "SERVICE_NAME" : str(request.form['ServiceName']),
            "REPLICAS" : int(request.form['Replicas']) ,
            #"SWARM_ID" : Swarm.query.filter_by(SWARM_NAME=str(request.form['SwarmId'])).with_entities(Swarm.SWARM_ID)
            #"IMAGE_ID": function of imageid ready from Image modle;
            #"IMAGENAME" : str(request.form['ImageName']),
            "HOSTPORT" :int(request.form['HostPort']),
            "CONTAINERPORT" :int(request.form['ContainerPort']),
            #"REGISTRY_ID": function of registry id
            #"DockerRegistry" : str(request.form['DockerRegistry']),
            #"CREATION_DATE":default date not required..
            #"Command" : str(request.form['Command']),
        }

        new_service = Service(**payload)

        try:


             db.session.add(new_service)

             db.session.commit()
             db.session.rollback()

        except exc.SQLAlchemyError:
            return render_template('page_500.html')

        return redirect(url_for('viewservice'))
    return render_template('createservice.html',names=registry_url)

@app.route('/tfoutput/<string:var>',methods=['GET'])
def tfoutput(var):
    email = 'sigmaxm2017@gmail.com'
    password = 'Ayappa2017'
    registered_user = User.query.filter_by(USERNAME=email).first()
    login_user(registered_user)
    session['user_id'] = registered_user.get_id()
    session['swarm_id'] = '63aacaf4-3534-4253-a3b5-051afa5079b8'
    session['tworking_dir'] = app.config["TF_WORKING_DIR"] + "/." + session['user_id'] + ":" + session['swarm_id']

    setsessTerraform(session, app.config)
    print tf_output(session,var)
    print tf_output(session,var)[0]
    return jsonify({'master_public_ips': tf_output(session,var)})


@app.route('/setsessTerraform/<string:swarm_name>',methods=['GET'])
def setterra(swarm_name):
    email = 'sigmaxm2017@gmail.com'
    registered_user = User.query.filter_by(USERNAME=email).first()
    login_user(registered_user)
    session['user_id'] = registered_user.get_id()
    session['swarm_id'] = Swarm.query.filter_by(SWARM_NAME=swarm_name).first()
    session['tworking_dir'] = app.config["TF_WORKING_DIR"] + "/." + session['user_id'] + ":" + session['swarm_id']
    print session
    #setsessTerraform(session, app.config)
    print 'tworking_dir = ' + session['tworking_dir']
    return jsonify(session['tworking_dir'])

## Function which needs some cleanup

# def backgroundimagedetails():
#     print session['user_id']
#     # Based on this user_id get the USER_ID -> REGISTRY_ID (registry URL)
#     reg = dockerregistry(app.config["REGISTRY_URL"])
#     imagedata = reg.registry_list()
#     imagedatalist = []
#     temp = {}
#     imagename = []
#     imagetag = []
#     for k, v in imagedata.items():
#         # print str(k)
#         for lv in v:
#             # print " ---" + str(lv)
#             temp['IMAGE_NAME'] = str(k)
#             temp['TAG'] = str(lv)
#             Image_name = str(k)
#             tagname = str(lv)
#
#             print str(Image_name)
#             print str(tagname)
#
#             _a = Image(IMAGE_ID=str(uuid.uuid4()),
#                        IMAGE_NAME=str(Image_name),
#                        REGISTRY_ID=str(uuid.uuid4()),
#                        TAG=str(tagname))
#             try:
#                _imagename = db.session.query(Image).filter_by(IMAGE_NAME=str(Image_name)).first()
#                _tagname = db.session.query(Image).filter_by(IMAGE_NAME=str(tagname)).first()
#                if not _imagename and not _tagname:
#                   # db.session.add(_a)
#                    runBackgroundJobs(db.session.add(_a))
#                    db.session.commit()
#             except exc.SQLAlchemyError:
#                print "Error"
