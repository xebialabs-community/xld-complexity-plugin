import requests
from requests.auth import HTTPBasicAuth
import json
from getpass import getpass

headers = { "Content-Type": "application/json", "Accept": "application/json" }

def get_Apps():
    reqURL = "%s/deployit/repository/v2/query?parent=Applications" % (URL)
    myResponse = requests.get(reqURL,headers=headers, auth=HTTPBasicAuth(username, password))
    if(myResponse.ok):
        print "getting Applications"
        applications = json.loads(myResponse.content)
        applications = get_directories(applications)
        for x in applications:
            reqURL = "%s/deployit/repository/v2/query?parent=%s" % (URL, x['ref'])
            myResponse = requests.get(reqURL,headers=headers, auth=HTTPBasicAuth(username, password))
            if(myResponse.ok):
                print "getting packages for " + x['ref']
                deployment_list = json.loads(myResponse.content)
                # for deployment in deployment_list:
                deployment_list = remove_CompositePackages(deployment_list)
                x['deployment_list'] = deployment_list
            else:
                print("Error code %s" % myResponse.status_code )
        for x in applications:
            deployments = x['deployment_list']
            for d in deployments:
                reqURL = "%s/deployit/repository/v2/query?parent=%s" % (URL, d['ref'])
                myResponse = requests.get(reqURL,headers=headers, auth=HTTPBasicAuth(username, password))
                if(myResponse.ok):
                    print "getting deployables for " + d['ref']
                    deployables = json.loads(myResponse.content)
                    d['deployables'] = len(deployables)
                else:
                    print("Error code %s" % myResponse.status_code )
        global DeploymentCount
        for x in applications:
            deployments = x['deployment_list']
            count = 0
            for d in deployments:
                if d['deployables'] > count:
                    count = d['deployables']
            DeploymentCount += count
        return DeploymentCount

def get_directories(applications):
    for apps in applications:
        if "Directory" in str(apps['type']):
            reqURL = "%s/deployit/repository/v2/query?parent=%s" % (URL, apps['ref'])
            myResponse = requests.get(reqURL,headers=headers, auth=HTTPBasicAuth(username, password))
            if(myResponse.ok):
                newApps = json.loads(myResponse.content)
                for newApp in newApps:
                    applications.append(newApp)
                applications.remove(apps)
                get_directories(applications)
    return applications

def remove_CompositePackages(applications):
    for apps in applications:
        if "udm.CompositePackage" in str(apps['type']):
            applications.remove(apps)
            remove_CompositePackages(applications)
    return applications

def remove_dictionaries(infrastructure):
    for infra in infrastructure:
        if "Dictionary" in str(infra['type']):
            infrastructure.remove(infra)
            remove_dictionaries(infrastructure)
        # elif  "udm.EncryptedDictionary" in str(infra.type):
        #     infrastructure.remove(infra)
        #     remove_dictionaries(infrastructure)
    return infrastructure

def get_Infra():
    global InfrastructureCount
    reqURL = "%s/deployit/repository/v2/query?parent=Environments" % (URL)
    myResponse = requests.get(reqURL,headers=headers, auth=HTTPBasicAuth(username, password))
    if(myResponse.ok):
        environments = json.loads(myResponse.content)
        environments = get_directories(environments)
        environments = remove_dictionaries(environments)
        for envs in environments:
            reqURL = "%s/deployit/repository/ci/%s" % (URL, envs['ref'])
            myResponse = requests.get(reqURL,headers=headers, auth=HTTPBasicAuth(username, password))
            if(myResponse.ok):
                infra = json.loads(myResponse.content)
                infra = infra['members']
                print "Getting infrastructure for " + envs['ref']
                for x in infra:
                    InfrastructureCount += 1
        return InfrastructureCount
    else:
        print("Error code %s" % myResponse.status_code )

URL = raw_input("Enter your URL : ")
username = raw_input("Enter your username : ")
password = getpass("password: ")
DeploymentCount =0
InfrastructureCount = 0
get_Apps()
get_Infra()
TotalScore = (DeploymentCount + InfrastructureCount)
print "|============================================|"
print "| Your total score is %s                     |" % TotalScore
print "| Your Application count score is %s         |" % DeploymentCount
print "| Your Environment count score is %s         |" % InfrastructureCount
print "| Please send this information to Digital.ai |"
print "| Thank you very much for your help          |"
print "|============================================|"
