from django import forms

from pages.models import Logfile 


class LogfileForm(forms.ModelForm):
    class Meta:
        model = Logfile 
        fields = ('logfile','uploaded_at', )
