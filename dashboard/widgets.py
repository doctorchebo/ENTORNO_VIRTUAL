from django import forms

class DatePickerInput(forms.DateInput):
    input_type = 'date'
class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'