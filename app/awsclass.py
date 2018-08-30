import boto3
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
