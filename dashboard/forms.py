from django import forms
from . models import *


#Notes Card
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']



#Homework Card

class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'deadline':DateInput()}
        fields = ['subject', 'title', 'description', 'deadline', 'is_finished']


#Youtube, Books Card

class DashboardFom(forms.Form):
    text = forms.CharField(max_length=100, label="Search:")

#ToDo Card
 
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
         