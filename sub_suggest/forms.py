#mindmap/forms.py
from django import forms
from .models import Sub_Suggest

class SuggestForm(forms.ModelForm):
    class Meta:
        model = Sub_Suggest
        fields = ['main_keyword']
        widgets = {
            'main_keyword': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color:#205959;color:white;'}),
        }
