#! /usr/bin/python
import commands
import os
import sys
import hashlib
import subprocess
import datetime
import shutil
dname = ''
dt = str(datetime.datetime.now())
MYDIR = os.path.abspath(os.path.dirname(__file__))
OPENSSL = '/usr/bin/openssl'
KEY_SIZE = 2048
DAYS = 3650
CA_CERT = 'ca.cert'
CA_KEY = 'ca.key'
dockerfile='/etc/sysconfig/docker'
#HOME=os.getenv("HOME")+'/.docker/'
HOME='/home/ec2-user/.docker'
BACKUP = dockerfile + dt

X509_EXTRA_ARGS = ()
USER=''
STR='2048'
ca=os.getenv("HOME")+'/.docker/ca.pem'
server=os.getenv("HOME")+'/.docker/server-cert.pem'
serverkey=os.getenv("HOME")+'/.docker/server-key.pem'    
class Tlscerts(object):
  __slots__ = ["val"]
  def __init__(self, value=''):
    self.val = value
  def setValue(self, value=None):
    self.val = value
    return value

  def Make(name, local=locals()):
      ret = GetVariable(name, local)
      if ret is None:
         ret = Tlscerts(0)
         globals()[name] = ret
      return ret   


def openssl(*args):
    cmdline = [OPENSSL] + list(args)
    subprocess.check_call(cmdline)

def gencert(domain, rootdir=MYDIR, keysize=KEY_SIZE, days=DAYS,HOME=HOME):
    def dfile(ext):
        return os.path.join('domains', '%s.%s' % (domain, ext))

    if not os.path.exists(HOME):
        os.mkdir(HOME)
    os.chdir(HOME)

    if (not os.path.isfile("ca.src") ):
       print(" => Creating ca.srl")
       subprocess.call('echo "01" >> ca.srl', shell=True)    


    print(" => Generating CA key")
    openssl('genrsa', '-out','ca-key.pem', str(keysize))

    openssl('req', '-new', '-key', 'ca-key.pem','-x509', '-days', str(days), '-nodes', '-subj' , '/CN='+domain, '-out', 'ca.pem')
    openssl('genrsa', '-out', 'server-key.pem', str(keysize))
    openssl('req', '-subj' , '/CN='+ domain, '-new','-key','server-key.pem','-out', 'server.csr')
    openssl('x509','-req','-days', str(days),'-in','server.csr','-CA','ca.pem','-CAkey','ca-key.pem','-out','server-cert.pem')
    openssl('genrsa', '-out', 'key.pem', str(keysize))
    openssl('req', '-subj' , '/CN=docker.client', '-new','-key','key.pem','-out', 'client.csr')
    subprocess.call('echo "extendedKeyUsage = clientAuth " >> extfile.cnf', shell=True)
    openssl('x509','-req','-days', str(days),'-in','client.csr','-CA','ca.pem','-CAkey','ca-key.pem','-out','cert.pem','-extfile','extfile.cnf')
    
    subprocess.call('rm -rf /home/ec2-user/client_docker', shell=True)
    subprocess.call('mkdir /home/ec2-user/client_docker', shell=True)
    subprocess.call('cp /home/ec2-user/.docker/ca.pem /home/ec2-user/client_docker/', shell=True)
    subprocess.call('cp /home/ec2-user/.docker/cert.pem /home/ec2-user/client_docker/', shell=True)
    subprocess.call('cp /home/ec2-user/.docker/key.pem /home/ec2-user/client_docker/', shell=True)

    subprocess.call('rm -f /home/ec2-user/client_docker.zip', shell=True)
    subprocess.call('cd /home/ec2-user/client_docker ; zip -r /home/ec2-user/client_docker.zip . ', shell=True)

    OPTIONS = """OPTIONS='--tlsverify --tlscacert=/home/ec2-user/.docker/ca.pem --tlscert=/home/ec2-user/.docker/server-cert.pem --tlskey=/home/ec2-user/.docker/server-key.pem -H=0.0.0.0:2376'"""
    bash = """
   #!/bin/bash
   export DOCKER_CERT_PATH=/home/ec2-user/.docker
   export DOCKER_HOST=tcp://%(dname)s:2376
   export DOCKER_TLS_VERIFY=1
  """
   
    move = shutil.move(dockerfile, BACKUP);
    config = open(dockerfile, 'w')
    config.write(OPTIONS % {'HOME':HOME})
    config.close()

if __name__ == "__main__":
    cmd = 'curl -s http://169.254.169.254/latest/meta-data/public-hostname'
    dname = commands.getoutput(cmd)
    gencert(str(dname))
    os.environ['DOCKER_HOST'] = "tcp://DOCKER_HOST:2376"
    os.environ['DOCKER_TLS_VERIFY'] = "1"
    subprocess.call('sudo service docker restart',shell=True)
    bash = """
#!/bin/bash
export DOCKER_CERT_PATH=/home/ec2-user/.docker
export DOCKER_HOST=tcp://%(dname)s:2376
export DOCKER_TLS_VERIFY=1
"""
    config = open('/etc/profile.d/docker.sh', 'w')
    config.write(bash % {'dname':dname})
    config.close()
    subprocess.call('sudo chmod +x /etc/profile.d/docker.sh',shell=True)
    subprocess.call('source /etc/profile.d/docker.sh',shell=True)
    print (" => Sucess fully created docker tls ! Please run docker info")
    

