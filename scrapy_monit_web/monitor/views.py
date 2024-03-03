from typing import List, Union

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.views.generic import View
from django.views.generic import ListView,CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.db.models.functions import Now


from .models import InstanceModel, JobModel, ProjectModel, SpiderModel
from .forms import AddInstanceForm
from .scrapyd_handlers import (get_all_active_jobs, get_IS, InstanceState, get_scrapyd_logs, FailedSpider,
                               )
from schedules.models import Schedule



def render_failed_spider(request, fail: FailedSpider):
    print("in fallen")
    context = {"url": fail.url, "message": fail.message}
    return render(request, 'monitor/fallen_instance.html', context)


class MainView(View):
    def __update_active_flag(self, instances: List[InstanceModel])->List[InstanceModel]:
        updateds = []
        for instance in instances:
            instance.active = instance.is_active()
            updateds.append(instance)
        return updateds
    
    def get(self, request: HttpRequest):
        content = {}
        if request.user.is_authenticated:
            instances = InstanceModel.objects.filter(author=request.user).all()
            instances = self.__update_active_flag(instances)
            if len(instances) != 0:
                # return states only for active instances
                instances_active = [instance for instance in instances if instance.active]
                states = get_IS(instances_active)
                assert len(instances_active) == len(states)
                instances_active = [save_state(model, state) for model, state in zip(instances_active, states)]

                # if fallen instance:
                failed_instances = [ins for ins in instances_active if isinstance(ins, FailedSpider)]
                if failed_instances:
                    return render_failed_spider(request, failed_instances[0])
                
                active_jobs = get_all_active_jobs(instances_active)

                content = {'instances': instances, 'actives': active_jobs}
            
        return render(request, 'monitor/main.html', content)

    

# CRUD Instance

class DetailInstanceView(View):
    def get(self, request: HttpRequest, name: str):
        instance = get_object_or_404(InstanceModel, name=name)
        active_jobs = instance.jobs.filter(status='running')
        context = {'instance': instance, 'actives': active_jobs}
        return render(request, 'monitor/instance_details.html', context)


class SpiderDetailView(View):
    def get(self, request: HttpRequest, name: str, spider_name):
        instance = get_object_or_404(InstanceModel, name=name)
        spider = get_object_or_404(SpiderModel, name=spider_name, instance=instance)
        active_jobs = instance.jobs.filter(status='running', spider=spider)
        context = {'spider': spider, 'actives': active_jobs}
        return render(request, 'monitor/spider_details.html', context)


class AddInstanceView(LoginRequiredMixin, CreateView):
    form_class = AddInstanceForm
    template_name = 'monitor/add_instance.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    context_object_name = 'form'


class UpdateInstanceView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = InstanceModel
    fields = ['name', 'address', 'description']
    template_name = 'monitor/update_instance.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    



class DeleteInstanceView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = InstanceModel
    template_name = 'monitor/delete.html'
    success_url = ''

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class JobDetailView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, instance_name: str, spider_name: str, job_id: str):
        job = get_object_or_404(JobModel, spider__name=spider_name, pk=job_id)
        logs = job.get_logs()
        context = {'job': job, 'logs': logs}
        return render(request, 'monitor/job_details.html', context)
    

class InstanceListView(LoginRequiredMixin, ListView):
    model = InstanceModel
    template_name = 'monitor/instance_list.html'
    context_object_name = 'instances'

    



def save_state(model: InstanceModel, state: InstanceState)->InstanceModel:
    """  """
    model.projects.all().delete()
    model.updated_at=Now()
    assert state.active is True
    # take care projects
    for project_s in state.projects:
        ProjectModel.objects.create(
            instance = model,
            name = project_s.name).save()
    # take care spiders
    # if scrapyd server is fallen
    if isinstance(state.spiders, FailedSpider): 
        return state.spiders

    else:
        for spider_s in state.spiders:
            project = ProjectModel.objects.get(name=spider_s.project.name, instance__name=spider_s.project.instance.name)
            schedules = Schedule.objects.filter(spider_identifier=spider_s.identifier)

            sp = SpiderModel.objects.create(
                project = project,
                instance = model,
                name = spider_s.name,
                identifier = spider_s.identifier,
            )
            sp.schedules.set(schedules)
            sp.save()

    # take care jobsget_IS
    for job_s in state.jobs:
        # retrieve project and spider
        project = ProjectModel.objects.get(instance__name=spider_s.project.instance.name, name=job_s.project.name)
        spider = SpiderModel.objects.get(name=job_s.spider.name, 
                                         project__name=project.name, 
                                         project__instance__name=job_s.project.instance.name)
        
        JobModel.objects.create(
            instance = model,
            id = job_s.id,
            pid = job_s.pid,
            spider = spider,
            project = project,
            started = job_s.start_time,
            ended = job_s.end_time,
            duration = job_s.duration,  
            status = job_s.status).save()
        
    return model


    
