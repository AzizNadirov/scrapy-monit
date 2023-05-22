from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.views.generic import View
from django.views.generic import ListView,CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.db.models.functions import Now


from .models import InstanceModel, JobModel, ProjectModel, Shedule, SpiderModel
from .forms import AddInstanceForm
from .scrapyd_handlers import get_all_active_jobs, get_IS, InstanceState




class MainView(View):
    def get(self, request: HttpRequest):
        content = {}
        if request.user.is_authenticated:
            instances = InstanceModel.objects.filter(author=request.user).all()
            if len(instances) != 0:
                states = get_IS(instances)
                assert len(instances) == len(states)
                instances = [save_state(model, state) for model, state in zip(instances, states)]
                active_jobs = get_all_active_jobs(instances)
                active_jobs=[]
                content = {'instances': instances, 'actives': active_jobs}
            
        return render(request, 'monitor/main.html', content)

    

# CRUD Instance

class DetailInstanceView(View):
    def get(self, request: HttpRequest, pk: int):
        instance = get_object_or_404(InstanceModel, id=pk)




class AddInstanceView(LoginRequiredMixin, CreateView):
    form_class = AddInstanceForm
    template_name = 'monitor/add_instance.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class UpdateInstanceView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
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
    



def save_state(model: InstanceModel, state: InstanceState)->InstanceModel:
    # new_instance = InstanceModel.objects.create(
    #     name =          model.name,
    #     description =   model.description,
    #     address =       model.address,
    #     created_at =    model.created_at)
    # new_instance.save()
    model.projects.all().delete()
    model.updated_at=Now()
    
    # take care projects
    for project_s in state.projects:
        ProjectModel.objects.create(
            instance = model,
            name = project_s.name).save()
    # take care projects
    for spider_s in state.spiders:
        project = ProjectModel.objects.get(name=spider_s.project.name)
        SpiderModel.objects.create(
            project = project,
            instance = model,
            name = spider_s.name
        ).save()
    # take care jobs
    for job_s in state.jobs:
        # retrieve project and spider
        project = ProjectModel.objects.get(name=job_s.project.name)
        spider = SpiderModel.objects.get(name=job_s.spider.name, project=project)
        JobModel.objects.create(
            instance = model,
            id = job_s.id,
            pid = job_s.pid,
            spider = spider,
            project = project,
            started = job_s.started,
            ended = job_s.ended,
            duration = job_s.duration,
            status = job_s.status).save()
    return model


    
