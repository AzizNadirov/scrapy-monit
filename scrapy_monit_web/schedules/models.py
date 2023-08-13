from datetime import datetime 
from datetime import timedelta 

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from monitor.validators import validate_cron_string



class TriggerOnceModel(models.Model):
    """ One-time trigger """
    start_at = models.DateTimeField('Start time', default=datetime.now() + timedelta(hours=12))
    del_end = models.BooleanField("Delete at the End", default=True)
    author = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"TriggerOnce: {self.start_at}"
    


class TriggerPeriodicModel(models.Model):
    start_at = models.DateTimeField('Start time', default=datetime.now())
    cron_str = models.CharField('Cron Pattern', max_length=60, validators=[validate_cron_string, ])
    author = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"TriggerPeriodic: from <{self.start_at}> as {self.cron_str} by - {self.author.user_name}"



class TriggerSequenceModel(models.Model):
    spiders = models.ManyToManyField('monitor.SpiderModel', related_name='seq_triggers', verbose_name='Spiders')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    trigger = GenericForeignKey('content_type', 'object_id')

    use_spider_start = models.BooleanField("Use Spider Start", default=True)
    detanator_spider = models.ForeignKey('monitor.SpiderModel', on_delete=models.SET_NULL, null=True, related_name='binded_seq_triggers')

    def __str__(self):
        spiders = [spider.name for spider in self.spiders.all()]
        return f"TriggerSequence[{self.trigger}] for [{spiders}]"



class TriggerModel(models.Model):
    name = models.CharField('Trigger', max_length=128)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    trigger = GenericForeignKey('content_type', 'object_id', for_concrete_model=True)
    
    status = models.BooleanField("Active", default=True)



    def get_absolute_url(self): # TODO
        return reverse("model_detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return f"<{self.name}: [{self.trigger}]>"



class Schedule(models.Model):
    name = models.CharField("Name", max_length=120)
    spider = models.ForeignKey('monitor.SpiderModel', on_delete=models.SET_NULL, null=True, related_name='shedules')
    author = models.ForeignKey("users.Profile", verbose_name="Author", on_delete=models.CASCADE, related_name='shedules')
    trigger = models.ForeignKey(TriggerModel, on_delete=models.SET_NULL, null=True, related_name='schedule')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField("Active", default=True)


    def get_absolute_url(self):
        return reverse("schedule_detail", kwargs={"pk": self.pk})
    


    # def __build_str(self):
    #     status = 'active' if self.is_active else 'inactive'
    #     if self.type in ('Once', 'once'):
    #         return f"<{status}>Once at {self.start_datetime}"
        
    #     elif self.type in ('Periodic', 'periodic'):
    #         return f"<{status}>Periodic every {self.period} hours"

    #     else:
    #         raise ValueError(f"Incorrect value for shedule type:'{self.type}'")


    # def __str__(self):
    #     return f"ScrapySpiderSheduler[{self.name}]: {self.__build_str()}"
