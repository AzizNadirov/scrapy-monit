from datetime import datetime 
from datetime import timedelta 

from django.db import models
from django.urls import reverse

from .scrapyd_handlers import InstanceState

from .scrapyd_handlers import get_scrapyd_logs, api_daemon_status





class InstanceModel(models.Model):
    """ ScrapyMonit instance model """
    name = models.CharField("Instance name", max_length=120)
    description = models.CharField("Description", max_length=255)
    address = models.URLField('Address')
    created_at = models.DateTimeField('Creatoin',auto_now_add = True)
    updated_at = models.DateTimeField('Updated', auto_now = True)
    author = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)


    
    def is_active(self)->bool:
        """check if instance daemon is running"""
        r = api_daemon_status(url=self.address)
        print(r is None)
        return not r is None

    
    def get_absolute_url(self):
        return reverse("instance_detail", kwargs={"name": self.name})
    


    def __str__(self):
        return f"ScrapyInstance: {self.name}"
    




class ProjectModel(models.Model):
    """ scrapyd project model """
    instance = models.ForeignKey(InstanceModel, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField('Name', default='default', max_length=120)
    version = models.CharField("Version", blank=True, max_length=120)

    def __str__(self) -> str:
        return f"ScrapyInstanceProject: {self.name} v:{self.version}"
    



class SpiderModel(models.Model):
    """ scrapyd spider model """
    instance = models.ForeignKey(InstanceModel, verbose_name='instance', on_delete=models.CASCADE, related_name='spiders')
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name='spiders')
    name = models.CharField("Name", max_length=120)
    triggers = models.ManyToManyField("schedules.TriggerModel", related_name='spiders', null=True)

    def get_absolute_url(self):
        return reverse("spider_detail", kwargs={"name": self.instance.name, 'spider_name': self.name})
    


    def __str__(self):
        return f"ScrapyProjectSpider: {self.name}"
    
    

class JobModel(models.Model):
    """ scrapyd job model """
    instance = models.ForeignKey(InstanceModel, verbose_name='instance', on_delete=models.CASCADE, related_name='jobs')
    id = models.CharField('id', max_length=120, primary_key=True)
    pid = models.CharField('pid', max_length=120, null=True)
    spider = models.ForeignKey(SpiderModel, verbose_name='spider', on_delete=models.CASCADE, related_name='jobs')
    project = models.ForeignKey(ProjectModel, verbose_name='project', on_delete=models.CASCADE, related_name='jobs')
    started = models.DateTimeField('started', auto_now=False, auto_now_add=False, null=True)
    ended = models.DateField('ended', auto_now=False, auto_now_add=False, null=True)
    duration = models.PositiveIntegerField('duration in minutes', null=True)
    status = models.CharField('status', max_length=50, choices=(('p', 'pending'), ('r', 'running'), ('f', 'finished')))

    def get_logs(self, project_name='default')->str:
        """returns logs of the job"""
        logs = get_scrapyd_logs(url=self.instance.address, project_name=project_name, spider_name=self.spider.name, job_id=self.id)
        return logs


    def get_absolute_url(self):
        kwargs = {"instance_name": self.instance.name, 'spider_name': self.spider.name, 'job_id': self.id}
        # print(f'reverse for: {kwargs}')
        return reverse("job_detail", kwargs=kwargs)
    
    
    def __str__(self):
        return f"ScrapyInstanceJob[{self.status}]: {self.instance.name}|{self.spider.name}"





    
