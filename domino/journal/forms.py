#Import User Modules
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Domino, List, Collection, Note, TimeBlock


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        #User Form saves in Database
        model = User
        fields = ["username", "email", "password1", "password2"]


class NewDominoForm(ModelForm):
    #def save(self, user):
    #    instance = super(NewDominoForm, self).save(commit=False)
    #    instance.author = user
    #    instance.save()
    #    self.save_m2m()
    #    return instance    
    #def save(self, user, parentId):
    #    instance = super(NewDominoForm, self).save(commit=False)
    #    instance.author = user
    #    instance.parentId = parentId
    #    instance.save()
    #    self.save_m2m()
    #    return instance    
    class  Meta:
        model = Domino
        fields = ['head', 'body', 'assignedJourney']
        widgets = {'DateCreated': forms.HiddenInput(), 'DateLastEditted': forms.HiddenInput()}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
    def __init__(self, user, *args, **kwargs):
         #self.author = kwargs.pop('author',None)
         super(NewDominoForm, self).__init__(*args, **kwargs)
         self.fields['assignedJourney'].queryset = Collection.objects.filter(author=user)


#Journey Creation
class NewJourneyForm(ModelForm):

    def __init__(self, *args, **kwargs):
         self.author = kwargs.pop('author',None)
         super(NewJourneyForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Collection
        fields=['journey','icon', 'description']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


#List Creation
class NewListForm(ModelForm):
    def __init__(self, *args, **kwargs):
         self.domino = kwargs.pop('domino',None)
         super(NewListForm, self).__init__(*args, **kwargs)
    class Meta:
        model = List
        fields =['content','domino','checked']
        widgets = {'domino': forms.HiddenInput(), 'checked': forms.HiddenInput()}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


#Note Creation
class NewNoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
         self.author = kwargs.pop('author',None)
         self.domino = kwargs.pop('domino',None)
         super(NewNoteForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Note
        fields =['content','domino',]
        widgets = {'domino': forms.HiddenInput(), 'author': forms.HiddenInput()}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


#Time Formats
class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


#time_input = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

class NewTimeForm(ModelForm):
    class Meta:
        model = TimeBlock
        fields = "__all__"
        widgets = {'domino': forms.HiddenInput(), 'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author',None)
        self.domino = kwargs.pop('domino',None)
        super(NewTimeForm, self).__init__(*args, **kwargs)
        self.fields['domino'].widget = forms.HiddenInput()
        self.fields['timeset'].widget = DateTimeInput()
        self.fields['timeset'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

