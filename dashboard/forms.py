from django import forms
from .models import *
from .widgets import DatePickerInput, DateTimePickerInput
import datetime

class DashboardForm(forms.Form):
    
    estado = (
        ('Pendiente','Pendiente'),
        ('Enviado','Enviado'),
        ('Recibido','Recibido'),
        ('Empatado','Empatado'),
    )
    fecha_inicial = forms.DateField(required=True, widget=DatePickerInput())
    fecha_final = forms.DateField(required=True, widget=DatePickerInput())
    estado = forms.ChoiceField(choices=estado, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        now = datetime.datetime.now()
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicial'].initial = now
        self.fields['fecha_final'].initial = now


