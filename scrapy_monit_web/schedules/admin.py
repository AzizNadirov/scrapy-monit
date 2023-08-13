from django.contrib import admin
from .models import (Schedule, TriggerModel, TriggerPeriodicModel, TriggerSequenceModel, TriggerOnceModel)



admin.site.register(Schedule)
admin.site.register(TriggerModel)
admin.site.register(TriggerPeriodicModel)
admin.site.register(TriggerSequenceModel)
admin.site.register(TriggerOnceModel)

