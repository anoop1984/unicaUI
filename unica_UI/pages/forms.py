from django import forms

from pages.models import Logfile_Testlab1
from pages.models import Logfile_Testlab2
from pages.models import adhocData 


class LogfileForm_Testlab1(forms.ModelForm):
    class Meta:
        model = Logfile_Testlab1
        fields = ('logfile','uploaded_at', )

class LogfileForm_Testlab2(forms.ModelForm):
    class Meta:
        model = Logfile_Testlab2
        fields = ('logfile','uploaded_at', )

class adhocData_Form(forms.ModelForm):
    class Meta:
        model = adhocData
        fields = ('site','timestamp','logfile','jsonfile',)
 
    
