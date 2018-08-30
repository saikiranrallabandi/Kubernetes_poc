--
docker build -t sigmaxm:latest .
docker run -d -p 5002:5002 sigmaxm

# bastion host 
ssh -i ~/.ssh/sigmaex2KeyPair.pem ubuntu@35.164.18.132

aws ec2 describe-images --image-ids ami-8cc43df4

--- Create dockerswarm-1
curl -i -u "admin" -p -H "Content-Type: application/json" -X POST -d '{ "KeyName" : "sigmaex2KeyPair", "ClusterSize":"2", "EnableCloudWatchLogs":"yes", "EnableSystemPrune":"no", "InstanceType":"t2.micro", "ManagerDiskSize":"20", "ManagerDiskType":"standard", "ManagerInstanceType":"t2.micro", "ManagerSize":"1", "WorkerDiskSize":"20", "WorkerDiskType":"standard" , "StackName" : "dockerswarm-1" }' http://localhost:5001/createStack

aws cloudformation describe-stacks --stack-name docker4

aws cloudformation list-stack-resources --stack-name dockerswarm-1 --output text --query 'StackResourceSummaries[*].{PhysicalResourceId:PhysicalResourceId,ResourceType:ResourceType==`AWS::AutoScaling::AutoScalingGroup`}'|grep True|grep -i Manager|awk '{print $1}'

aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name dockerswarm-1-ManagerAsg-4T6Q4M93GGFA  --query "AutoScalingGroups[*].Instances[*].InstanceId" --output=text

aws ec2 describe-instances  --instance-ids i-050a428e34be54b37 --query "Reservations[*].Instances[*].PublicIpAddress" --output=text


--- Create dockerswarm-2
curl -i -u "admin" -p -H "Content-Type: application/json" -X POST -d '{ "KeyName" : "sigmaex2KeyPair", "ClusterSize":"2", "EnableCloudWatchLogs":"yes", "EnableSystemPrune":"no", "InstanceType":"t2.micro", "ManagerDiskSize":"20", "ManagerDiskType":"standard", "ManagerInstanceType":"t2.micro", "ManagerSize":"1", "WorkerDiskSize":"20", "WorkerDiskType":"standard" , "StackName" : "dockerswarm-2" }' http://localhost:5001/createStack

aws cloudformation describe-stacks --stack-name dockerswarm-1

# Connect to dockerswarm-1
ssh -i ~/.ssh/sigmaex2KeyPair.pem ubuntu@<swarm1-ip>

# visualizer 
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer

#-- dockerswarm-1
docker login -u sigmaex2 
docker login -u admin sigmaxm.com

docker service create --detach=false --with-registry-auth --publish 5000:5000 --replicas 4 --name flaskapp sigmaxm.com/flaskapp:latest
docker service scale flaskapp=4
docker service ls flaskapp

#--- Changes to app.py
( Version change deploy to dockerswarm-2 ) 




#-- dockerswarm-2
docker login -u sigmaex2 
docker login -u admin sigmaxm.com
docker service create --detach=false --with-registry-auth --publish 5000:5000 --replicas 4 --name flaskapp sigmaxm.com/flaskapp:latest
docker service scale flaskapp=4
docker service ls flaskapp

---- Load balance listener command
aws elb delete-load-balancer-listeners --load-balancer-name docker4aw-External-14AZJ6SNL79DH --load-balancer-ports 5000
aws elb create-load-balancer-listeners --load-balancer-name docker4aw-External-14AZJ6SNL79DH --listeners "Protocol=TCP,LoadBalancerPort=5000,InstanceProtocol=TCP,InstancePort=5050"

aws elb delete-load-balancer-listeners --load-balancer-name docker4aw-External-14AZJ6SNL79DH --load-balancer-ports 5000
aws elb create-load-balancer-listeners --load-balancer-name docker4aw-External-14AZJ6SNL79DH --listeners "Protocol=TCP,LoadBalancerPort=5000,InstanceProtocol=TCP,InstancePort=5060"

-----

curl -i -u "admin" -p -H "Content-Type: application/json" -X POST -d '{ "ManagerIP" : "54.244.70.194", "ImageName":"nginx", "ServiceName" : "nginx", "Replicas": 4 , "PublishPort" :"80:80" }' http://localhost:5001/deployService

-- working with feature/siva branch
