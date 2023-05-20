from django import forms
from .models import InstanceModel




class AddInstanceForm(forms.ModelForm):
    class Meta:
        model = InstanceModel
        fields = ['name', 'address', 'description']
        widgets = {'tags': forms.TextInput(attrs={'class': 'form-control'})}