from typing import List, Union, Optional, Tuple, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta

from .scrapyd_api import (api_daemon_status, api_delproject, api_delversion, api_list_projects, api_listjobs,
                          api_listspiders, api_listversions, get_scrapyd_logs, run_scrapy_spider, subdict)




@dataclass
class InstanceSchema:
    name: str
    address: str


@dataclass
class ProjectSchema:
    name: str
    instance: InstanceSchema


@dataclass
class SpiderSchema:
    name: str
    instance: InstanceSchema
    project: ProjectSchema



@dataclass
class JobSchema:
    """ duration in hour """
    id: int
    spider: SpiderSchema
    project: ProjectSchema
    status: str
    instance: InstanceSchema = None
    pid: int = None
    started: datetime = None
    ended: datetime = None
    duration: int = None


class InstanceHandler:
    def __init__(self, instance):
        self.name:      str =                   instance.name
        self.url:       str =                   instance.address
        self.__schema:  InstanceSchema =        InstanceSchema(self.name, self.url)
        self.active:    bool =                  None
        self.projects:  List[ProjectSchema] =   None
        self.spiders:   List[SpiderSchema] =    None
        self.jobs:      List[JobSchema] =       None

        if not self.check_deamon():
            raise ValueError("Instance daemon is not active.")
        else:
            self.active = True
        
        self.projects = self.get_projects()
        self.spiders = self.get_spiders()
        self.jobs = self.get_joblist()



    def __parse_job(self, jobs_dict: dict)->List[JobSchema]:
        """ converts 'api_listjob' response into list of Jobs """
        types_fields = {'pending': ['project', 'spider', 'id', 'pid', 'start_time'], 
                        'running': ['project', 'spider', 'id', 'pid', 'start_time'], 
                        'finished': ['project', 'spider', 'id', 'start_time', 'end_time']}
        
        jobs = []
        
        for type in types_fields.keys():
            jobs: List[dict] = jobs_dict[type]
            for job in jobs:
                j = JobSchema(**types_fields[type])
                if j.started:   j.started =     datetime.strptime(j.started)
                if j.ended:     j.ended =       datetime.strptime(j.ended)

                if type == 'finished':
                    j.duration = j.ended - j.started
                j.instance = self.__schema
                j.project = ProjectSchema(name=j.project, instance=self.__schema)
                j.spider = SpiderSchema(name=j.spider, project=j.project)
                jobs.append(j)

        return jobs
    

    
    def check_deamon(self) -> bool:
        """ returns True if deamon is active """
        r = api_daemon_status(self.url)
        return r['status'] == 'ok'
    

    def get_projects(self) -> List[ProjectSchema]:
        """ returns list of project names """
        r = api_list_projects(self.url)
        if not r:
            return None
        return [ProjectSchema(name=proj, instance=self.__schema) for proj in r]
    

    def get_spiders(self) -> List[SpiderSchema]:
        """ returns list of spiders """
        assert not self.projects is None
        spiders = []
        for project in self.projects:
            r = api_listspiders(url=self.url, project=project.name)
            if r is None:
                return None
            for spider in r:
                spider.append(SpiderSchema(name=spider, instance=self.__schema, project=project))

        return spiders
    

    def run_spider(self, name: str, project_name: str='default') -> bool:
        """ shedule spider """
        if not name in [spider.name for spider in self.spiders]:
            return False
        
        if not project_name in [project_name.name for project in self.projects]:
            return False
        
        return run_scrapy_spider(url=self.url, spider_name=name, project_name=project_name)
        


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



def get_all_active_jobs(*instances: Tuple[InstanceHandler], top_n=5) -> dict:
    res = {}
    for instance in instances:
        ih = InstanceHandler(instance)
        res[instance.name] = [job for job in ih.jobs if job.status == 'running']
        res[instance.name].sort(key=(lambda j: j.started), reverse=True )
        res[instance.name] = res[instance.name][: top_n]

    return res
    


