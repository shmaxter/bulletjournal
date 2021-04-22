from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


#Timeline Requirement
from django.utils import timezone


#Collection
class Collection(models.Model):
    journey = models.CharField(max_length=225)
    DateCreated = models.DateTimeField(default=timezone.now)
    icon = models.CharField(max_length=255, blank = True)
    description = models.TextField(blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default = 1)
    #magic method
    def __str__(self):
        return self.journey

#Domino Types: Note, File, 
class Type(models.Model):
    name = models.CharField(max_length=255, default='domino')
    icon = models.CharField(max_length=255, default='circle')
    def __str__(self):
        return self.name

# Create your models here.
class Domino(models.Model):
    head = models.CharField(max_length=255)
    body = models.TextField(blank= True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastEditted = models.DateTimeField(default=timezone.now)
    #DateCompleted = models.DateTimeField(null=True, blank= True)
    #DatePinned = models.DateTimeField(null=True, blank= True)
    #DateCompleted = models.DateTimeField(blank=True)
    #Status(Pinned, Checked)    
    #User Link  
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    assignedJourney = models.ManyToManyField(Collection, blank=True)
    #thisJourney = models.ForeignKey(Collection, models.SET_NULL, blank=True, null=True)
    #dominoType = models.ForeignKey(Type,null=True,blank=True, on_delete=models.CASCADE)
    parentId = models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE)
    isPinned = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)
    #Time Set
    timeset = models.BooleanField(default=False)
    #magic method
    def __str__(self):
        return self.head

    def journey_name(self):
        return self.assignedJourney.company_name



#CheckList
class List(models.Model):
    content = models.CharField(max_length=500)
    domino = models.ForeignKey(Domino, on_delete=models.CASCADE, blank=True)    
    checked = models.BooleanField(default=False)
    def __str__(self):
        return self.content


class TimeBlock(models.Model):
    domino = models.ForeignKey(Domino, on_delete=models.CASCADE, blank=True)
    timeset = models.DateTimeField(auto_now=False, auto_now_add=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255, blank = True)


#Note
class Note(models.Model):
    title = models.CharField(max_length=225, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    domino = models.ForeignKey(Domino, on_delete=models.CASCADE, blank=True)    



#Comments