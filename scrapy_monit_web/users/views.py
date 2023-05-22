from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .forms import UserRegistrationForm, ProfileUpdateForm
from monitor.models import InstanceModel




class ProfileView(LoginRequiredMixin, View):
    RECENT_NUM = 5
    def get(self, request):
        user = request.user
        instance_queryset = InstanceModel.objects.filter(author__id=user.id).order_by('-created_at')[:self.RECENT_NUM]
        context = {'instances': instance_queryset}
        return render(request, 'users/profile.html', context=context)



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('user_name')
            messages.success(request, f'You are registered successfully! Now you can log in !')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'users/register.html',{'form': form} )



@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated successfully!')
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user)

    context = {'form':form}
    return render(request, 'users/edit_profile.html', context)
