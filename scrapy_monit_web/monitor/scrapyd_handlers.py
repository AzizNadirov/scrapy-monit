from typing import List, Union, Sequence, Tuple, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from django.db.models import QuerySet

from .exceptions import InstanceIsInactive
from .scrapyd_api import (api_daemon_status, api_list_projects, api_listjobs, api_listspiders, 
                          get_scrapyd_logs, run_scrapy_spider, FailedSpider, cancel_scrapy_spider)


@dataclass
class InstanceSchema:
    name: str
    address: str


@dataclass
class ProjectSchema:
    name: str
    instance: InstanceSchema



@dataclass
class TriggerSchema:
    name: str = None
    author: str = None
    status: bool = None



@dataclass
class SpiderSchema:
    name: str
    project: ProjectSchema
    identifier: str
    triggers: List[TriggerSchema] = None
    jobs = ...


@dataclass
class JobSchema:
    """ duration in hour """
    id: int
    status: str
    spider: SpiderSchema
    project: ProjectSchema
    instance: InstanceSchema = None
    pid: int = None
    start_time: datetime = None
    end_time: datetime = None
    duration: int = None
    log_url: str = None
    items_url: str = None




class InstanceState:
    def __init__(self, instance_model):
        self.name:      str =                   instance_model.name
        self.url:       str =                   instance_model.address
        self.__schema:  InstanceSchema =        InstanceSchema(self.name, self.url)
        self.active:    bool =                  None
        self.projects:  List[ProjectSchema] =   None
        self.spiders:   List[SpiderSchema] =    None
        self.jobs:      List[JobSchema] =       None
        self.failed: bool = False

        if not self.check_deamon():
            self.active = False
        else:
            self.active = True
            self.projects = self.get_projects()
            self.spiders = self.get_spiders()
            self.jobs = self.get_joblist()

            # if scrapyd server is fallen
            if isinstance(self.spiders, FailedSpider): self.failed = True 



    def __parse_job(self, jobs_dict: dict)->List[JobSchema]:
        """ converts 'api_listjob' response into list of Jobs """
        types_fields = {'pending': ['project', 'spider', 'id', 'pid', 'start_time'], 
                        'running': ['project', 'spider', 'id', 'pid', 'start_time'], 
                        'finished': ['project', 'spider', 'id', 'start_time', 'end_time', 'log_url', 'items_url']}
        
        jobs_res = []
        
        for status in types_fields.keys():
            jobs: List[dict] = jobs_dict[status]
            for job in jobs:
                job['status'] = status
                j = JobSchema(**job)
                format = '%Y-%m-%d %H:%M:%S.%f'
                if j.start_time:   j.start_time =     datetime.strptime(j.start_time, format)
                if j.end_time:     j.end_time =       datetime.strptime(j.end_time, format)

                if status == 'finished':
                    j.duration = j.end_time - j.start_time
                    j.duration = j.duration.total_seconds() / 60
                j.instance = self.__schema
                j.project = ProjectSchema(name=j.project, instance=self.__schema)
                j.spider = SpiderSchema(name=j.spider, project=j.project, identifier=f"{j.instance.name}:{j.spider}")
                jobs_res.append(j)

        return jobs_res
    
    
    def check_deamon(self) -> bool:
        """ returns True if deamon is active """
        r = api_daemon_status(self.url)
        if r is None: return None
        return r['status'] == 'ok'
    

    def get_projects(self) -> List[ProjectSchema]:
        """ returns list of project names """
        r = api_list_projects(self.url)
        if not r:
            return None
        return [ProjectSchema(name=proj, instance=self.__schema) for proj in r]
    

    def get_spiders(self) -> List[SpiderSchema] | None | FailedSpider:
        """ returns list of spiders """
        assert not self.projects is None
        spiders = []
        for project in self.projects:
            r = api_listspiders(url=self.url, project=project.name)
            if isinstance(r, FailedSpider):
                return r
            for spider in r:
                spiders.append(SpiderSchema(name=spider, project=project, identifier=f"{self.name}:{spider}"))

        return spiders
    

    def run_spider(self, name: str, project_name: str='default') -> bool:
        """ shedule spider """
        if not name in [spider.name for spider in self.spiders]:
            return False
        
        if not project_name in [project_name.name for project in self.projects]:
            return False
        
        return run_scrapy_spider(url=self.url, spider_name=name, project_name=project_name)
    

    def cancel_spider(self, spider_name: str, project_name: str='default') -> bool:
        """ cancel spider """
        if not spider_name in [spider.name for spider in self.spiders]:
            return False
        
        if not project_name in [project_name.name for project in self.projects]:
            return False
        
        return cancel_scrapy_spider(url=self.url, job_id=spider_name, project_name=project_name)


    def get_joblist(self)-> List[JobSchema]:
        """ returns list of jobs """  
        jobs = []
        for project in self.projects:
            r = api_listjobs(url=self.url, project=project.name)
            if r['status'] != 'ok':
                return None
        
            jobs.extend(self.__parse_job(r))

        return jobs
    

    def get_logs(self, spider_name: str, job_id: str, project_name: str='default'):
        return get_scrapyd_logs(url=self.url, project_name=project_name,spider_name=spider_name, job_id=job_id)


def get_IS(instance_models: Sequence)->List[InstanceState]:
    """ takes Instance models and returns list of instance states """
    # assert instance_models

    states = [InstanceState(model) for model in instance_models]
    return states



def get_all_active_jobs(instances, top_n: int =5) -> dict:
    """ takes list of InstanceModel and return dict as Dict[instance.name: List[job]] """

    res = {}
    for instance in instances:
        if not instance.active:
            continue
        res[instance.name] = [job for job in instance.jobs.filter(status='running')]
        res[instance.name].sort(key=(lambda j: j.started), reverse=True )
        res[instance.name] = res[instance.name][: top_n]

    return res

