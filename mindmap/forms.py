#mindmap/forms.py
from django import forms
from .models import MindMap

class MindMapForm(forms.ModelForm):
    class Meta:
        model = MindMap
        fields = ['main_keyword']
        widgets = {
            'main_keyword': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color:#205959;color:white;'}),
        }
