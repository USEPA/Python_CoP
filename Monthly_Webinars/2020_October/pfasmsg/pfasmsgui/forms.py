from django.forms import ModelForm

from .models import PFASMsgRecord

class PFASMsgForm(ModelForm):
    class Meta:
        model = PFASMsgRecord
        exclude = ['ip', 'timestamp']
