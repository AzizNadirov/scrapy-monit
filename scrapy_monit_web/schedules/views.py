from typing import List, Union

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.views.generic import View
from django.views.generic import ListView,CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Schedule, TriggerModel, TriggerPeriodicModel, TriggerOnceModel, TriggerSequenceModel



class MainScheduleView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        schedules = Schedule.objects.filter(is_active=True).all()
        context = {'schedules': schedules}
        return render(request, 'schedules/main.html', context)




class ScheduleDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        context = {'schedule': schedule}
        return render(request, 'schedules/schedule_detail.html', context)
