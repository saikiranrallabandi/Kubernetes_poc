from flask_bcrypt import generate_password_hash

from database import db
import datetime
import bcrypt
from flask_login import UserMixin

def _get_date():
    return datetime.datetime.now()


class User(UserMixin,db.Model):
    __tablename__ = "XM_USER"
    id = db.Column(db.String(128), primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column('USERNAME', db.String(128), unique=True, index=True)
    PASSWORD = db.Column('PASSWORD', db.String(128))
    #CREATION_DATE = db.Column('CREATION_DATE', db.DateTime)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def __init__(self, id,USERNAME, PASSWORD ):
        self.id = id
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        #self.CREATION_DATE = datetime.utcnow()

    def set_password(self, PASSWORD):
        self.PASSWORD = generate_password_hash(PASSWORD)

    def check_password(self, password):
        if bcrypt.hashpw(password.encode('utf8'), self.PASSWORD.encode('utf8')) == self.PASSWORD.encode('utf8'):
            print "It matches"
            return True
        else:
            return False
            print "It does not match"

        return check_password_hash(self.PASSWORD, PASSWORD)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.USERNAME)



class RigisterUser(UserMixin,db.Model):
    __tablename__ = "XM_REGISTERUSER"
    id = db.Column(db.String(128), primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column('USERNAME', db.String(128), unique=True, index=True)
    PASSWORD = db.Column('PASSWORD', db.String(128))
    #CREATION_DATE = db.Column('CREATION_DATE', db.DateTime)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def __init__(self, id,USERNAME, PASSWORD ):
        self.id = id
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        #self.CREATION_DATE = datetime.utcnow()

    def set_password(self, PASSWORD):
        self.PASSWORD = generate_password_hash(PASSWORD)

    def check_password(self, password):
        if bcrypt.hashpw(password.encode('utf8'), self.PASSWORD.encode('utf8')) == self.PASSWORD.encode('utf8'):
            print "It matches"
            return True
        else:
            return False
            print "It does not match"

        return check_password_hash(self.PASSWORD, PASSWORD)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.USERNAME)


class AWSConfig(db.Model):
    __tablename__ = 'XM_AWSCONFIG'
    AWSCONFIG_ID = db.Column(db.String(128), primary_key=True)
    AWS_ACCESS_KEY_ID = db.Column(db.String(128), nullable=False)
    AWS_SECRET_ACCESS_KEY = db.Column(db.String(128), nullable=False)
    AWS_REGION_NAME = db.Column(db.String(128), nullable=False)
    AWS_ACCOUNT_ID = db.Column(db.Integer, nullable=False)
    USER_ID = db.Column(db.String(128), nullable=False)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def get_account_id(self):
        return unicode(self.AWS_ACCOUNT_ID)

    #def as_dict(self):
    #    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    #@property
    #def json(self):
    #    return to_json(self, self.__class__)

    def __repr__(self):
        return '<AWSCONFIG (%s, %s) >' % (self.AWSCONFIG_ID,self.AWS_ACCOUNT_ID)

class Registry(db.Model):
    __tablename__ = 'XM_REGISTRY'
    REGISTRY_ID = db.Column(db.String(128), primary_key=True)
    REGISTRY_URL = db.Column(db.String(128), nullable=False)
    REGISTRY_PORT = db.Column(db.Integer, nullable=False)
    REGISTRY_USERNAME = db.Column(db.String(128), nullable=False)
    REGISTRY_PASSWORD = db.Column(db.String(128), nullable=False)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def __repr__(self):
        return '<Registry (%s, %s) >' % (self.REGISTRY_ID,self.REGISTRY_URL)

class Registry_User(db.Model):
    __tablename__ = 'XM_REGISTRY_USER'
    ASSOCIATION_ID = db.Column(db.String(128), primary_key=True)
    REGISTRY_ID = db.Column(db.String(128), nullable=False)
    id = db.Column(db.String(128),nullable = False )

    def __repr__(self):
        return '<Registry_User (%s, %s) >' % (self.id,self.REGISTRY_ID)

#class Image(db.Model):
#    pass

#class Stack(db.Model):
#    pass

class Swarm(db.Model):
    __tablename__ = 'XM_SWARM'
    SWARM_ID = db.Column(db.String(128), primary_key=True)
    SWARM_NAME = db.Column(db.String(128), nullable=False)
    SWARM_STATUS  = db.Column(db.String(128), nullable=False)
    KEYNAME = db.Column(db.String(128), nullable=False)
    # Manager details
    MANAGERSIZE = db.Column(db.Integer, nullable=False)
    MANAGERINSTANCETYPE = db.Column(db.String(128), nullable=False)
    MANAGERDISKTYPE = db.Column(db.String(128), nullable=False)
    MANAGERDISKSIZE = db.Column(db.Integer, nullable=False)
    # WorkerDetails details
    CLUSTERSIZE = db.Column(db.Integer, nullable=False)
    INSTANCETYPE = db.Column(db.String(128), nullable=False)
    WORKERDISKTYPE = db.Column(db.String(128), nullable=False)
    WORKERDISKSIZE = db.Column(db.Integer, nullable=False)
    # Misc
    ENABLECLOUDWATCHLOGS = db.Column(db.String(128), nullable=False)
    ENABLESYSTEMPRUNE  = db.Column(db.String(128), nullable=False)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    #def __init__(self,swarmid):
    #    self.SWARM_ID = swarmid

    def __repr__(self):
        return '<Swarm (%s, %s) >' % (self.SWARM_ID,self.SWARM_NAME)

class Manager_Details(db.Model):
    __tablename__ = 'XM_MANAGER_DETAILS'
    MANAGER_ID = db.Column(db.String(128), primary_key=True)
    SWARM_ID  = db.Column(db.Integer)
    MANAGER_HOSTNAME = db.Column(db.String(128), nullable=True)
    MANAGER_IP = db.Column(db.String(128), nullable=True)
    MANAGER_STATUS = db.Column(db.String(128), nullable=True)
    ENGINE_VERSION =  db.Column(db.String(128), nullable=False)
    AVAILABILITY  = db.Column(db.String(128), nullable=False)
    MANAGER_STATE = db.Column(db.String(128), nullable=False)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def __repr__(self):
        return '<ManagerDetails (%s, %s) >' % (self.MANAGER_ID,self.MANAGER_HOSTNAME)

class Worker_Details(db.Model):
    __tablename__ = 'XM_WORKER_DETAILS'
    WORKER_ID = db.Column(db.String(128), primary_key=True)
    SWARM_ID  = db.Column(db.String(128))
    WORKER_HOSTNAME = db.Column(db.String(128), nullable=True)
    WORKER_IP = db.Column(db.String(128), nullable=True)
    WORKER_STATUS = db.Column(db.String(128), nullable=True)
    ENGINE_VERSION =  db.Column(db.String(128), nullable=False)
    AVAILABILITY  = db.Column(db.String(128), nullable=False)
    WORKER_STATE = db.Column(db.String(128), nullable=False)
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def __repr__(self):
        return '<WorkerDetails (%s, %s) >' % (self.WORKER_ID,self.WORKER_HOSTNAME)

#class Docker_Swarm(db.Model):
#    pass

#class K8S_Swarm(db.Model):
#    pass

class Service(db.Model):
    __tablename__ = 'XM_SERVICE'
    SERVICE_ID = db.Column(db.String(128), primary_key=True)
    SERVICE_NAME  = db.Column(db.String(128), nullable=True)
    REPLICAS =  db.Column(db.Integer)
    SWARM_ID  = db.Column(db.String(128))
    IMAGE_ID  = db.Column(db.String(128))
    HOSTPORT =  db.Column(db.Integer)
    CONTAINERPORT =  db.Column(db.Integer)
    REGISTRY_ID  = db.Column(db.String(128))
    CREATION_DATE = db.Column(db.Date, default=_get_date)

    def __repr__(self):
        return '<Service (%s, %s) >' % (self.SERVICE_ID,self.SERVICE_NAME)


def to_list_of_json(i, c):

    def to_json(inst,cls):
        convert = dict()
        d = dict()
        for c in cls.__table__.columns:
            v = getattr(inst, c.name)
            if c.type in convert.keys() and v is not None:
                try:
                    d[c.name] = convert[c.type](v)
                except:
                    d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
            elif v is None:
                d[c.name] = str()
            else:
                d[c.name] = v
        return d

    a_l=[]
    for l in i:
        a_l.append(to_json(l, c))

    return a_l
