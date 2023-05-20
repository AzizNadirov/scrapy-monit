from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.views.generic import View
from django.views.generic import ListView,CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import InstanceModel
from .forms import AddInstanceForm




class MainView(View):
    def get(self, request: HttpRequest):
        content = {'user_': 'Aziz'}
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
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.added_by
    



class DeleteInstanceView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = InstanceModel
    template_name = 'monitor/delete.html'
    success_url = ''

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.added_by