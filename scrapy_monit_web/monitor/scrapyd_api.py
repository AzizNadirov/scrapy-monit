# scrapyd API functions

import requests
from typing import List, Tuple, Union, Optional




def subdict(_dict: dict, keys: Union[list, tuple]):
    return {k: _dict[k] for k in keys}



def api_daemon_status(url: str):
    url = f"{url}/daemonstatus.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        fields = ["status","running", "pending", "finished", "node_name"]
        return subdict(data, fields)
    else:
        return None
    

def api_list_projects(url: str):
    url = f"{url}/listprojects.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['projects']
    else:
        return None
    

def api_listversions(url: str, project: str='default'):
    """  """
    url = f"{url}/listversions.json"
    # check if project in projects
    assert project in api_list_projects()
    params = {'project': project}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['versions']
    else:
        return None


def api_listspiders(url: str, project: str='default', _version: str=None)-> List[str]:
    """  """
    endp = f"{url}/listspiders.json"
    # check if project in projects
    projects = api_list_projects(url)
    if not projects is None:
        assert project in projects
        if not _version is None:
            assert _version in api_listversions(project)
        params = {'project': project, '_version': _version}
        response = requests.get(endp, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['spiders']
        else:
            return None
    else: 
        return None
    

def api_listjobs(url: str, project: str='default') -> dict:
    """ 
        {
            "status": "ok",
            "pending": [
                {
                    "project": "myproject", "spider": "spider1",
                    "id": "78391cc0fcaf11e1b0090800272a6d06"
                }
            ],
            "running": [
                {
                    "id": "422e608f9f28cef127b3d5ef93fe9399",
                    "project": "myproject", "spider": "spider2",
                    "start_time": "2012-09-12 10:14:03.594664"
                }
            ],
            "finished": [
                {
                    "id": "2f16646cfcaf11e1b0090800272a6d06",
                    "project": "myproject", "spider": "spider3",
                    "start_time": "2012-09-12 10:14:03.594664",
                    "end_time": "2012-09-12 10:24:03.594664",
                    "log_url": "/logs/myproject/spider3/2f16646cfcaf11e1b0090800272a6d06.log",
                    "items_url": "/items/myproject/spider3/2f16646cfcaf11e1b0090800272a6d06.jl"
                }
            ]
        }
    """
    endp = f"{url}/listjobs.json"
    # check if project in projects
    assert project in api_list_projects(url)

    params = {'project': project}
    response = requests.get(endp, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def api_delversion(_version: str, project: str='default'):
    """  """
    url = f"{url}/delversion.json"
    # check if project in projects
    assert project in api_list_projects()
    assert _version in api_listversions(project)

    params = {'project': project, '_version': _version}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['status']
    else:
        return None
    

def api_delproject(url: str, project: str):
    """  """
    url = f"{url}/delproject.json"
    # check if project in projects
    assert project in api_list_projects()
    params = {'project': project}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['status']
    else:
        return None
    

def get_scrapyd_logs(url: str, project_name: str, spider_name: str, job_id: str):
    """ returns log of job """
    
    url = f"{url}/logs/{project_name}/{spider_name}/{job_id}.log"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Exception: status code got: {response.status_code}")
    



def run_scrapy_spider(url: str, spider_name: str, project_name: str='default')->bool:
    """ run spider """
    assert spider_name in api_listspiders(url=url, project=project_name)

    schedule_url = f'{url}/schedule.json'
    response = requests.post(schedule_url, data={'project': project_name, 'spider': spider_name})
    if response.status_code == 200:
        print('Spider scheduled successfully.')
        return True
    else:
        print('Spider scheduling failed.')
        return False











