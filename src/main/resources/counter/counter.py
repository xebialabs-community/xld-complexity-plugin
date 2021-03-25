    #
    # Copyright 2020 XEBIALABS
    # Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    # The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json

import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Counter")

InfrastructureCount = 0
DeploymentCount = 0
infraSum = []
appSum = []
def get_deployables():
    master_list = []
    applications = repositoryService.query(None, "Applications", "", "", None, None, 0, 0)
    deployment_list = []
    deployables = []
    applications = get_directories(applications)
    master_list = convert(applications)
    for x in master_list:
        deployment_list = (repositoryService.query(None, x['id'], "", "", None, None, 0, 0))
        deployment_list = remove_CompositePackages(deployment_list)
        x['deployment_list'] = convert(deployment_list)
    for x in master_list:
        deployments = x['deployment_list']
        for d in deployments:
            deployables = repositoryService.query(None, d['id'], "", "", None, None, 0, 0)
            logger.info(str(deployables))
            d['deployables'] = len(deployables)

    global DeploymentCount
    for x in master_list:
        a = {}
        deployments = x['deployment_list']
        count = 0
        for d in deployments:
            if d['deployables'] > count:
                count = d['deployables']
        DeploymentCount += count
        a['count'] = count
        logger.info(str(x['id']))
        a['name'] = str(x['id'])
        name = a['name']
        name = name.replace('/',' ')
        a['name'] = name
        # logger.info(str(a))
        appSum.append(a)
        #logger.info("Deployables for Application: %s is %s" % (x['id'], count))

def get_directories(applications):
    for apps in applications:
        if "Directory" in str(apps.type):
            newApps = repositoryService.query(None, apps.id, "", "", None, None, 0, 0)
            applications += (newApps)
            applications.remove(apps)
            get_directories(applications)
    return applications

def remove_dictionaries(infrastructure):
    for infra in infrastructure:
        if "Dictionary" in str(infra.type):
            infrastructure.remove(infra)
            remove_dictionaries(infrastructure)
        # elif  "udm.EncryptedDictionary" in str(infra.type):
        #     infrastructure.remove(infra)
        #     remove_dictionaries(infrastructure)
    return infrastructure

def remove_CompositePackages(applications):
    for apps in applications:
        if "udm.CompositePackage" in str(apps.type):
            applications.remove(apps)
            remove_CompositePackages(applications)
    return applications

def convert(list):
    dict = []
    for a in list:
        temp = {}
        temp['id'] = a.id
        temp['type'] = a.type
        dict.append(temp)
    return dict

def get_infrastructure():
    global infraSum
    infrastructure = repositoryService.query(None, "Environments", "", "", None, None, 0, 0)
    infrastructure = get_directories(infrastructure)
    infrastructure = remove_dictionaries(infrastructure)
    for infra in infrastructure:
        a ={}
        i = 0
        env = repositoryService.read(str(infra.id))
        env = env.getProperty("members")
        global InfrastructureCount
        for x in env:
            InfrastructureCount += 1
            i +=1
        a['count'] = i
        a['name'] = str(infra.id)
        name = a['name']
        name = name.replace('/',' ')
        a['name'] = name
        logger.info(str(a))
        infraSum.append(a)


get_infrastructure()
get_deployables()
response.entity = {"status": "OK", "infraSum": infraSum, "appSum": appSum, "ApplicationsComplexScore": DeploymentCount,
"InfrastructureComplexScore": InfrastructureCount, "TotalScore": DeploymentCount+InfrastructureCount}
