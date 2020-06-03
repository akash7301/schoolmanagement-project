from django import forms
from django.forms import modelformset_factory,BaseModelFormSet
from corecode.models import AcademicSession,AcademicTerm,Subject

from .models import Result

class CreateResult(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),widget=forms.CheckboxSelectMultiple)

EditResult = modelformset_factory(Result,fields=('test_score','exam_score'),extra=0,can_delete=True)
