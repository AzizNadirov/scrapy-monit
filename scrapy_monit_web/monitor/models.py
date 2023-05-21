from django.db import models
from django.urls import reverse





class InstanceModel(models.Model):
    name = models.CharField("Instance name", max_length=120)
    description = models.CharField("Description", max_length=255)
    address = models.URLField('Address')
    created_at = models.DateTimeField('Creatoin',auto_now_add = True)
    updated = models.DateTimeField('Updated', auto_now = True)
    added_by = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"ScrapyInstance: {self.name}"



class ProjectModel(models.Model):
    instance = models.ForeignKey(InstanceModel, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField('Name', default='default', max_length=120)
    version = models.CharField("Version", blank=True, max_length=120)

    def __str__(self) -> str:
        return f"ScrapyInstanceProject: {self.name} v:{self.version}"
    



class SpiderModel(models.Model):
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=120)

    def __str__(self):
        return f"ScrapyProjectSpider: {self.name}"
    

class JobModel(models.Model):
    instance = models.ForeignKey(InstanceModel, verbose_name='instance', on_delete=models.CASCADE, related_name='jobs')
    id = models.CharField('id', max_length=120, primary_key=True)
    pid = models.CharField('pid', max_length=120, null=True)
    spider = models.ForeignKey(SpiderModel, verbose_name='spider', on_delete=models.CASCADE, related_name='jobs')
    project = models.ForeignKey(ProjectModel, verbose_name='project', on_delete=models.CASCADE, related_name='jobs')
    started = models.DateTimeField('started', auto_now=False, auto_now_add=False, null=True)
    ended = models.DateField('ended', auto_now=False, auto_now_add=False, null=True)
    duration = models.PositiveIntegerField('duration in minutes')
    status = models.CharField('status', max_length=50, choices=(('p', 'pending'), ('r', 'running'), ('f', 'finished')))


    def get_absolute_url(self):
        return reverse("", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"ScrapyInstanceJob[{self.status}]: {self.instance.name}|{self.spider.name}"


class Shedule(models.Model):
    name = models.CharField("Name", max_length=120)
    spider = models.ForeignKey(SpiderModel, on_delete=models.CASCADE, related_name='shedules')
    author = models.ForeignKey("users.Profile", verbose_name="Author", on_delete=models.SET_NULL, null=True, related_name='shedules')
    type = models.CharField(choices=(('Once', 'once'), ('Periodic', 'periodic')), default='Periodic', max_length=60)
    start_datetime = models.DateTimeField('Once Start DateTime', null=True)
    period = models.PositiveIntegerField("Period in hours", null=True)
    is_active = models.BooleanField("Active", default=True)



    def __build_str(self):
        status = 'active' if self.is_active else 'inactive'
        if self.type in ('Once', 'once'):
            return f"<{status}>Once at {self.start_datetime}"
        
        elif self.type in ('Periodic', 'periodic'):
            return f"<{status}>Periodic every {self.period} hours"

        else:
            raise ValueError(f"Incorrect value for shedule type:'{self.type}'")


    def __str__(self):
        return f"ScrapySpiderSheduler[{self.name}]: {self.__build_str()}"
    