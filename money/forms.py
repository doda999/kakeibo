from django import forms
from .models import Expence, Category_out, Revenue, Category_in

class ExpenceCreate(forms.ModelForm):
    class Meta:
        model = Expence
        fields = (
            'date', 'detail', 'user', 'cost', 'category',
        )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['user'].widget.attrs['hidden'] = 'true'
        self.fields['date'].widget.input_type = "date"

class ExpenceUpdate(forms.ModelForm):
    class Meta:
        model = Expence
        fields = (
            'date', 'detail','cost', 'category',
        )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.input_type = "date"

class RevenueCreate(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = (
            'date', 'detail', 'user', 'cost', 'category',
        )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['user'].widget.attrs['hidden'] = 'true'
        self.fields['date'].widget.input_type = 'date'
    
class RevenueUpdate(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = (
            'date', 'detail', 'cost', 'category',
        )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.input_type = "date"



