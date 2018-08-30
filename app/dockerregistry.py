import json
import requests
import sys

''' Disable Warnings when using verify=False'''
'''requests.packages.urllib3.disable_warnings()'''

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
