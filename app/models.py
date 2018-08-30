import hashlib
from flask import Flask, url_for, request, render_template
from flask.ext.mysql import MySQL

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL()
mysql.init_app(app)


def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()


def validate(username, password):
    completion = False
    connection = mysql.connect()
    cur = connection.cursor()

    cur.execute("select * from users where username = %s", username)
    auth = cur.fetchall()
    cur.close()
    for row in auth:
        dbUser = row[1]
        dbPass = row[2]
        if dbUser == username:
            completion = check_password(dbPass, password)

    connection.close()
    return completion


def putawsconfigdata(AccessKey, SeceretKey, Region, AWSAccountID):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT IFNULL(Max(id),0) FROM awsconfig;''')
    maxid = cur.fetchone()
    id = maxid[0] + 1
    cur.execute(
        """insert into awsconfig (id, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME,AWS_Account_ID) VALUES (%s,%s,%s,%s,%s)""",
        (id, str(AccessKey), str(SeceretKey), str(Region), AWSAccountID));
    connection.commit()
    connection.close()


def getawsconfigdata():
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT * FROM awsconfig;''')
    # https://geert.vanderkelen.org/2010/fetching-rows-as-dictionaries-with-mysql-connectorpython/
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    for row in cur:
        data.append(dict(zip(mycolumns, row)))

    # data = cur.fetchall()
    columns = [
        {
            "field": "id",
            "title": "id",
            "sortable": True,
        },
        {
            "field": "AWS_Account_ID",  # which is the field's name of data key
            "title": "AWS_Account_ID",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "AWS_ACCESS_KEY_ID",
            "title": "AWS_ACCESS_KEY_ID",
            "sortable": True,
        },
        {
            "field": "AWS_REGION_NAME",
            "title": "AWS_REGION_NAME",
            "sortable": True,
        },
    ]


    connection.close()
    return data, columns


def putregistrydata(registry, registry_username, registry_password):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT IFNULL(Max(id),0) FROM registry;''')
    maxid = cur.fetchone()
    id = maxid[0] + 1
    cur.execute(
        """insert into registry (id, registry, registry_username,registry_password) VALUES (%s,%s,%s,%s)""",
        (id, str(registry), str(registry_username), str(registry_password)));
    connection.commit()
    connection.close()
    return None


def getregistrydata():
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT id,registry,registry_username FROM registry order by id asc;''')
    # https://geert.vanderkelen.org/2010/fetching-rows-as-dictionaries-with-mysql-connectorpython/
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    for row in cur:
        data.append(dict(zip(mycolumns, row)))

    # data = cur.fetchall()
    columns = [
        { "field": "id", "title": "ID", "sortable": True, },
        { "field": "registry", "title": "Registry", "sortable": False, },
        { "field": "registry_username",  "title": "RegistryUsername",  "sortable": True, }
    ]

    connection.close()
    return data, columns

def getregistrydetails(registry):
    connection = mysql.connect()
    cur = connection.cursor()
    #cur.execute('''SELECT * FROM registry;''')
    cur.execute("select registry_username,registry_password from registry where registry=%s LIMIT 1", registry)
    data = cur.fetchone()
    registry_username = data[0]
    registry_password = data[1]
    cur.close()

    return registry_username, registry_password


def putservicedata(SwarmName,SwarmURL,ServiceName,ImageName,HostPort,ContainerPort,DockerRegistry,Replicas):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT IFNULL(Max(ServiceId),0) FROM service;''')
    maxid = cur.fetchone()
    ServiceId = maxid[0] + 1
    cur.execute(
        """insert into service (ServiceId, SwarmName,SwarmURL,ServiceName,ImageName,HostPort,ContainerPort,DockerRegistry,Replicas ) 
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (ServiceId, str(SwarmName),str(SwarmURL),str(ServiceName),str(ImageName),HostPort,ContainerPort,str(DockerRegistry),Replicas ));
    connection.commit()
    connection.close()
    return None

def getswarmdict(port=8080):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT swarmname ,CONCAT('http://',CONCAT(CONCAT(trim(dnsname),':')),%s) as dnsname FROM swarm ;''',port)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    connection.close()
    ddict={}
    for d in data :
        ddict[str(d['swarmname'])]=str(d['dnsname'])
    print ddict
    return ddict


def getservicedata():
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT service.ServiceId as ServiceId, service.SwarmName as SwarmName,ServiceName,ImageName,HostPort,ContainerPort,Replicas,CONCAT('http://',CONCAT(CONCAT(dnsname,':')),HostPort) as dnsname FROM service , swarm where service.SwarmName = swarm.SwarmName;''')
    # https://geert.vanderkelen.org/2010/fetching-rows-as-dictionaries-with-mysql-connectorpython/
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    #print mycolumns
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    #data.sort()
    print data
    # data = cur.fetchall()
    columns = [
        { "field": "Action", "title": "<input type='checkbox'  name='select_all' value='1' id='example'></input>","defaultContent":"<input type='checkbox' name='select_all' value='1' id='example' ></input>", "sortable": True,},
        { "field": "ServiceId", "title": "ServiceId", "sortable": True,},
        { "field": "SwarmName", "title": "SwarmName", "sortable": True,},
        { "field": "ServiceName", "title": "ServiceName", "sortable": True,},
        { "field": "ImageName", "title": "ImageName", "sortable": True,},
        { "field": "HostPort", "title": "HostPort", "sortable": True,},
        { "field": "ContainerPort", "title": "ContainerPort", "sortable": True,},
        { "field": "Replicas", "title": "Replicas", "sortable": True,},
        { "field": "dnsname", "title": "EndPoint", "sortable": True,},
    ]

    connection.close()
    return data, columns

def deleteservicedata(ServiceId):
    print "deleting service id " + str(ServiceId)
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("delete from service where ServiceId=%s ", ServiceId)
    cur.fetchall()
    connection.commit()
    connection.close()
    return ServiceId


def getserviceiddata(ServiceId):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT service.SwarmName as SwarmName,ServiceName,CONCAT('http://',CONCAT(CONCAT(dnsname,':')),HostPort) as dnsname FROM service , swarm where service.SwarmName = swarm.SwarmName and service.ServiceId = %s;''',ServiceId)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    connection.close()
    return data


def putswarmdata(stackid,swarmname,createdate,workerdisksize,enablecloudwatchlogs,managerdisksize,enablesystemprune,clustersize,keyname,managerdisktype,managersize,workerdisktype,instancetype,managerinstancetype,stackstaus):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("""insert into swarm (stackid,swarmname,createdate,workerdisksize,enablecloudwatchlogs,managerdisksize,enablesystemprune,clustersize,keyname,managerdisktype,managersize,workerdisktype,instancetype,managerinstancetype,stackstaus)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
        (str(stackid), str(swarmname),createdate,str(workerdisksize),str(enablecloudwatchlogs),str(managerdisksize),str(enablesystemprune),str(clustersize),str(keyname),str(managerdisktype),str(managersize),str(workerdisktype),str(instancetype),str(managerinstancetype),str(stackstaus))) 
    connection.commit()
    connection.close()
    return None

def deleteswarmdata(SwarmID):
    print "deleting SwarmID id " + str(SwarmID)
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("delete from swarm where stackid=%s ", SwarmID)
    cur.fetchall()
    connection.commit()
    connection.close()
    return SwarmID

def getdockerswarmdata():
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT stackid as stackid,swarmname FROM swarm ''')
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    columns = [
        {"field": "", "title": "<input type='checkbox' name='select_all' id='example' value='1'></input>", "defaultContent": "<input type='checkbox' id='example' name='select_all' value='1' ></input>",
         "sortable": False, },
        #{"field": "Action", "title": "Action", "sortable": True, },
        {"field": "Action","sortable": False, "data": '', "defaultContent": "<button class='btn btn-info btn-sm' id='details'>View Details</button>", "title": "Action"
         },
        { "field": "stackid", "title": "SwarmID", "sortable": True,},
        { "field": "swarmname", "title": "SwarmName", "sortable": True,}
    ]
    connection.close()
    return data, columns

def getviewswarmdetails():
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute('''SELECT stackid,SwarmName,createdate,dnsname from swarm''')
    # https://geert.vanderkelen.org/2010/fetching-rows-as-dictionaries-with-mysql-connectorpython/
    Swarmdata_info = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    # print mycolumns
    for row in cur:
        Swarmdata_info.append(dict(zip(mycolumns, row)))
    # data.sort()
    print Swarmdata_info

    cur.execute('''SELECT managerinstancetype,managersize,managerdisktype from swarm''')
    # https://geert.vanderkelen.org/2010/fetching-rows-as-dictionaries-with-mysql-connectorpython/
    Swarm_mangerdata_info = []
    Swarm_mangercoloums_info = tuple([d[0].decode('utf8') for d in cur.description])
    # print mycolumns
    for row in cur:
        Swarm_mangerdata_info.append(dict(zip(Swarm_mangercoloums_info, row)))
    # data.sort()
    print "saikiran"
    print Swarm_mangerdata_info
    cur.execute('''SELECT instancetype,workerdisksize,clustersize from swarm''')
    # https://geert.vanderkelen.org/2010/fetching-rows-as-dictionaries-with-mysql-connectorpython/
    Swarm_workerdata_info = []
    Swarmcoloum__Worker = tuple([d[0].decode('utf8') for d in cur.description])
    # print mycolumns
    for row in cur:
        Swarm_workerdata_info.append(dict(zip(Swarmcoloum__Worker, row)))
    # data.sort()
    print Swarm_workerdata_info



    Swarm_info = [
        {"field": "stackid", "title": "stackid", "sortable": True, },
        {"field": "SwarmName", "title": "SwarmName", "sortable": True, },
        {"field": "createddate", "title": "createddate", "sortable": True, },
        {"field": "dnsname", "title": "dnsname", "sortable": True, }
    ]

    Swarm_Manager = [
        {"field": "managerinstancetype", "title": "managerinstancetype", "sortable": True},
        {"field": "managersize", "title": "managersize", "sortable": True },
        {"field": "managerdisktype", "title": "managerdisktype", "sortable": True}

        ]

    Manger_server = [
        {"field": "ID", "title": "ID", "sortable": True},
        {"field": "Hostname", "title": "Hostname", "sortable": True},
        {"field": "Address", "title": "Address", "sortable": True},
        {"field": "Engine Version", "title": "Engine Version", "sortable": True},
        {"field": "Availability", "title": "Availability", "sortable": True},
        {"field": "State", "title": "State", "sortable": True}
    ]

    Swarm_Worker = [
        {"field": "instancetype", "title": "instancetype", "sortable": True, },
        {"field": "workerdisksize", "title": "workerdisksize", "sortable": True, },
        {"field": "workerdisktype", "title": "workerdisktype", "sortable": True, },
        {"field": "clustersize", "title": "clustersize","sortable":True}

        ]
    worker_server = [
        {"field": "Hostname", "title": "Hostname", "sortable": True},
        {"field": "Address", "title": "Address", "sortable": True},
        {"field": "Engine Version", "title": "Engine Version", "sortable": True},
        {"field": "Availability", "title": "Availability", "sortable": True},
        {"field": "State", "title": "State", "sortable": True}
    ]

    connection.close()
    return Swarmdata_info,Swarm_mangerdata_info,Swarm_workerdata_info,Swarm_info,Swarm_Manager,Swarm_Worker







def registryhost():
    registry_host = []
    connection = mysql.connect()
    cur = connection.cursor()
    #cur.execute("select * from registry where registry_username=%s", registry_username)
    cur.execute("select * from registry ")
    auth = cur.fetchall()
    cur.close()
    for row in auth:
        host = row[1]
        print host
        registry_host.append(host)
    print registryhost
    connection.close()
    return registry_host


def getdashboardData():
    connection = mysql.connect()
    cur = connection.cursor()
    dashboardData = {}
    #cur.execute('''SELECT IFNULL(Max(id),0) FROM awsconfig;''')
    cur.execute('''SELECT count(*) FROM awsconfig;''')
    maxid = cur.fetchone()
    acount=maxid[0]
    cur.execute('''SELECT count(*) FROM swarm;''')
    maxid = cur.fetchone()
    swarmcount=maxid[0]
    cur.execute('''SELECT count(*) FROM service;''')
    maxid = cur.fetchone()
    servcount=maxid[0]
    dashboardData = {'awsaccount': acount, 'dockerswarms': swarmcount, 'containers': '?', 'services': servcount}
    connection.close()
    return  dashboardData


# Siva Changes(1.0)
def getswarminfo(swamname):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("SELECT stackid,SwarmName,createdate,dnsname from swarm where SwarmName=%s",swamname)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    #print mycolumns
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    #data.sort()
    #print data
    # data = cur.fetchall()
    columns = [
        {"field": "stackid", "title": "stackid", "sortable": True, },
        {"field": "SwarmName", "title": "SwarmName", "sortable": True, },
        {"field": "createddate", "title": "createddate", "sortable": True, },
        {"field": "dnsname", "title": "dnsname", "sortable": True, }
    ]
    connection.close()
    return data, columns

def getmanagerinfo(swamname):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("SELECT managerinstancetype,managerdisktype,managersize  from swarm where SwarmName=%s",swamname)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    #print mycolumns
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    #data.sort()
    print data
    # data = cur.fetchall()
    columns = [
        {"field": "managerinstancetype", "title": "managerinstancetype", "sortable": True, },
        {"field": "managerdisktype", "title": "managerdisktype", "sortable": True, },
        {"field": "managersize", "title": "managersize", "sortable": True, },
    ]
    connection.close()
    return data, columns

def getmanagerdetailsinfo(swamname):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("SELECT managerhostname,managerip,engineversion,availablity,state  from managerdetails , swarm where managerdetails.swarmid=swarm.stackid and swarm.swarmname = %s",swamname)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    #print mycolumns
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    #data.sort()
    print data
    # data = cur.fetchall()
    columns = [
        {"field": "managerhostname", "title": "managerhostname", "sortable": True, },
        {"field": "managerip", "title": "managerip", "sortable": True, },
        {"field": "engineversion", "title": "engineversion", "sortable": True, },
        {"field": "availablity", "title": "availablity", "sortable": True, },
        {"field": "state", "title": "state", "sortable": True, },
    ]
    connection.close()
    return data, columns

def getworkerinfo(swamname):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("SELECT instancetype,workerdisktype,clustersize  from swarm where SwarmName=%s",swamname)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    #print mycolumns
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    #data.sort()
    print data
    # data = cur.fetchall()
    columns = [
        {"field": "instancetype", "title": "instancetype", "sortable": True, },
        {"field": "workerdisktype", "title": "workerdisktype", "sortable": True, },
        {"field": "clustersize", "title": "clustersize", "sortable": True, },
    ]
    connection.close()
    return data, columns

def getworkderdetailsinfo(swamname):
    connection = mysql.connect()
    cur = connection.cursor()
    cur.execute("SELECT workerhostname,workerip,state  from workerdetails , swarm where workerdetails.swarmid=swarm.stackid and swarm.swarmname = %s",swamname)
    data = []
    mycolumns = tuple([d[0].decode('utf8') for d in cur.description])
    #print mycolumns
    for row in cur:
        data.append(dict(zip(mycolumns, row)))
    #data.sort()
    print data
    # data = cur.fetchall()
    columns = [
        {"field": "workerhostname", "title": "workerhostname", "sortable": True, },
        {"field": "workerip", "title": "workerip", "sortable": True, },
        {"field": "state", "title": "state", "sortable": True, },
    ]
    connection.close()
    return data, columns

