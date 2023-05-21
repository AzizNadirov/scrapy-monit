from django.contrib import admin
from .models import InstanceModel, ProjectModel, SpiderModel, Shedule, JobModel


admin.site.register(InstanceModel)
admin.site.register(ProjectModel)
admin.site.register(SpiderModel)
admin.site.register(Shedule)
admin.site.register(JobModel)

