from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Domino, List, Collection, Note, TimeBlock
#Import User Modules
from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, NewDominoForm, NewListForm, NewJourneyForm, NewNoteForm, NewTimeForm
#IterTool Chains for merging Models together
from itertools import chain
#Calendar Module
import calendar, datetime
from calendar import HTMLCalendar


# Create your views here.

def index(request):
    #Query Dominos
    user = request.user
    pinneddominos = Domino.objects.filter(author=user.id, isPinned = True).prefetch_related('assignedJourney').order_by('-DateLastEditted')
    dominos = Domino.objects.filter(author=user.id, isPinned = False, parentId__isnull=True, isCompleted = False).prefetch_related('assignedJourney').order_by('-id')
    completeddominos = Domino.objects.filter(author=user.id, isPinned = False, parentId__isnull=True, isCompleted = True).prefetch_related('assignedJourney').order_by('-DateLastEditted')
    journeys = Collection.objects.filter(author = user.id).order_by('id')    
    return render(request, 'journal/dominos.html', {'user':user, 'dominos':dominos,'completeddominos':completeddominos, 'pinneddominos':pinneddominos, 'journeys': journeys})
    #return HttpResponse("hi")

def domino(request, domino_id):
    #Query Dominos
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    #List Load
    #lists = List.objects.filter(domino=domino)
    #Notes Load
    notes = Note.objects.filter(author=user.id,domino=domino)
    #List Form
    listform = NewListForm()
    #dominos In Progress..
    dominos = Domino.objects.filter(author=user.id, isPinned = False, parentId = domino).order_by('id')
    pinneddominos = Domino.objects.filter(author=user.id, isPinned = True, parentId = domino).order_by('-id')
    
    #new variable notedoms
    notedoms = sorted(
        chain(dominos, notes),
        key = lambda notedom: notedom.DateCreated, reverse = False)

    timedoms = TimeBlock.objects.filter(domino=domino)
    return render(request, 'journal/domino.html', {'user':user, 'domino':domino, 'listform':listform, 'notes': notes, 'dominos': dominos, 'pinneddominos': pinneddominos, 'notedoms': notedoms, 'timedoms': timedoms})
    #return HttpResponse("hi")



def new(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        assignedJourneys = request.POST.getlist('checks[]')
        #if(data['journey_new'] != ''):
        #    journey, created = Collection.objects.get_or_create(journey=data['journey_new'],user=user)
        
        domino = Domino.objects.create(
            head = data['title'],
            body = data['body'],
            #parentId = null,
            author = user,
        )
        domino.assignedJourney.set(assignedJourneys)
        domino.save()
        rediredturl = '/domino/id/' + str(domino.id)
        return redirect(rediredturl)                  
    else:        
        user = request.user
        assignedJourneys = Collection.objects.filter(author = user.id).order_by('id')
        return render(request, 'journal/newdomino.html', {"assignedJourneys":assignedJourneys})






#Update Domino
def newsub(request, domino_id):
    if request.method == 'POST':
        user = request.user
        prentdomino = Domino.objects.get(author=user.id,id = domino_id)
        data = request.POST
        assignedJourneys = request.POST.getlist('checks[]')
        #if(data['journey_new'] != ''):
        #    journey, created = Collection.objects.get_or_create(journey=data['journey_new'],user=user)
        
        domino = Domino.objects.create(
            head = data['title'],
            body = data['body'],
            parentId = prentdomino,
            author = user,
        )
        domino.assignedJourney.set(assignedJourneys)
        domino.save()
        rediredturl = '/domino/id/' + str(domino.id)
        return redirect(rediredturl)
    else:
        user = request.user
        prentdomino = Domino.objects.get(author=user.id,id = domino_id)
        assignedJourneys = Collection.objects.filter(author = user.id).order_by('id')
        dominojourneys = prentdomino.assignedJourney.all()
        assignedJourneys = [x for x in assignedJourneys if x not in dominojourneys]
        return render(request, 'journal/editdomino.html', {"assignedJourneys":assignedJourneys,"dominojourneys":dominojourneys})






#Update Domino
def update(request, domino_id):
    if request.method == 'POST':
        user = request.user
        domino = Domino.objects.get(author=user.id,id = domino_id)
        data = request.POST
        assignedJourneys = request.POST.getlist('checks[]')
        #if(data['journey_new'] != ''):
        #    journey, created = Collection.objects.get_or_create(journey=data['journey_new'],user=user)
        
        domino.head = data["title"]
        domino.body = data["body"]
        domino.assignedJourney.set(assignedJourneys)
        domino.save()
        rediredturl = '/domino/id/' + str(domino.id)
        return redirect(rediredturl)
    else:
        user = request.user
        domino = Domino.objects.get(author=user.id,id = domino_id)
        assignedJourneys = Collection.objects.filter(author = user.id).order_by('id')
        dominojourneys = domino.assignedJourney.all()
        assignedJourneys = [x for x in assignedJourneys if x not in dominojourneys]
        return render(request, 'journal/editdomino.html', {"domino":domino,"assignedJourneys":assignedJourneys,"dominojourneys":dominojourneys})



#Update Domino
def newJourneyDomino(request, journey_id):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        assignedJourneys = request.POST.getlist('checks[]')
        #if(data['journey_new'] != ''):
        #    journey, created = Collection.objects.get_or_create(journey=data['journey_new'],user=user)
        
        domino = Domino.objects.create(
            head = data['title'],
            body = data['body'],
            #parentId = prentdomino,
            author = user,
        )
        domino.assignedJourney.set(assignedJourneys)
        domino.save()
        rediredturl = '/domino/journey/' + str(journey_id)
        return redirect(rediredturl)
    else:
        user = request.user
        #assignedJourney = Collection.objects.get(id=journey_id)
        journey = Collection.objects.get(author=user.id,id = journey_id)
        assignedJourneys = Collection.objects.filter(author = user.id).exclude(id = journey_id).order_by('id')
        #assignedJourneys = [x for x in assignedJourneys if x not assignedJourney]
        return render(request, 'journal/journeydomino.html', {"assignedJourneys":assignedJourneys, "journey": journey})


def newnote(request, domino_id):
    if request.method == 'POST':
        user = request.user
        form = NewNoteForm(request.POST)        
        if form.is_valid():   
            newnote = form.save(commit=False)
            notedomino = Domino.objects.get(author=user.id,id = domino_id)
            newnote.domino = notedomino
            newnote.author = user
            newnote.save()
            rediredturl = '/domino/id/' + str(domino_id)
            return redirect(rediredturl)       
    else:
        noteform = NewNoteForm()
        domino_id = str(domino_id)
        return render(request, 'journal/newnote.html', {'noteform': NewNoteForm, 'domino_id': domino_id})

def newtime(request, domino_id):
    if request.method == 'POST':
        user = request.user
        form = NewTimeForm(request.POST)        
        if form.is_valid():   
            newtime = form.save(commit=False)
            timedomino = Domino.objects.get(author=user.id,id = domino_id)
            newtime.domino = timedomino
            newtime.author = user
            newtime.save()
            if timedomino.timeset == False:
                timedomino.timeset = True
                timedomino.save()
            rediredturl = '/domino/id/' + str(domino_id)
            return redirect(rediredturl)       
    else:
        #Initiate Form
        timeform = NewTimeForm()
        domino_id = str(domino_id)
        return render(request, 'journal/newtime.html', {'timeform': NewTimeForm, 'domino_id': domino_id})

def pin(request, domino_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isPinned):
        domino.isPinned = False
    else:
        domino.isPinned = True
    domino.DateLastEditted = timezone.now()
    domino.save()
    rediredturl = '/domino/id/' + str(domino_id)
    return redirect(rediredturl)

def pinParent(request, domino_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isPinned):
        domino.isPinned = False
    else:
        domino.isPinned = True
        domino.isCompleted = False
    domino.DateLastEditted = timezone.now()
    domino.save()
    rediredturl = '/domino/id/' + str(domino.parentId.id) + '#d' + str(domino.id)
    return redirect(rediredturl)
    #rediredturl = '/domino/id/' + str(domino.parentId.id)
    #return redirect(rediredturl)

def pinHome(request, domino_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isPinned):
        domino.isPinned = False
    else:
        domino.isPinned = True
        domino.isCompleted = False
    domino.DateLastEditted = timezone.now()
    domino.save()    
    rediredturl = '/domino#d' + str(domino_id)
    return redirect(rediredturl)
    #rediredturl = '/domino/'    
    #return redirect(rediredturl)


def pinJourney(request, domino_id, journey_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isPinned):
        domino.isPinned = False
    else:
        domino.isPinned = True
        domino.isCompleted = False
    domino.DateLastEditted = timezone.now()
    domino.save()
    rediredturl = '/domino/journey/' + str(journey_id)
    return redirect(rediredturl)

def completeHome(request, domino_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isCompleted):
        domino.isCompleted = False
    else:
        domino.isCompleted = True
        domino.isPinned = False
    domino.DateLastEditted = timezone.now()
    domino.save()
    #rediredturl = '/domino#d' + str(domino_id)
    rediredturl = '/domino'
    return redirect(rediredturl)

def completeParent(request, domino_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isCompleted):
        domino.isCompleted = False
    else:
        domino.isCompleted = True
        domino.isPinned = False
    domino.DateLastEditted = timezone.now()
    domino.save()
    rediredturl = '/domino/id/' + str(domino.parentId.id) + '#d' + str(domino.id)
    return redirect(rediredturl)


def completeJourney(request, domino_id, journey_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isCompleted):
        domino.isCompleted = False
    else:
        domino.isCompleted = True
        domino.isPinned = False
    domino.DateLastEditted = timezone.now()
    domino.save()
    rediredturl = '/domino/journey/' + str(journey_id)
    return redirect(rediredturl)


def complete(request, domino_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    if(domino.isCompleted):
        domino.isCompleted = False
    else:
        domino.isCompleted = True
        domino.isPinned = False
    domino.DateLastEditted = timezone.now()
    domino.save()
    rediredturl = '/domino/id/' + str(domino.id)
    return redirect(rediredturl)

def listitem(request, list_id):
    user = request.user
    listitem = List.objects.get(author=user.id,id = list_id)
    if(listitem.checked):
        listitem.checked = False
    else:        
        listitem.checked = True
    listitem.save()
    rediredturl = '/domino/id/' + str(listitem.domino.id)
    return redirect(rediredturl)

        


def journey(request, journey_id):
    #Query Dominos
    user = request.user
    journeys = Collection.objects.filter(author = user.id).exclude(id = journey_id).order_by('id')    
    journey = Collection.objects.get(author=user.id,id = journey_id)
    journeySelected = True;    
    pinneddominos = Domino.objects.filter(author=user.id, isPinned = True, assignedJourney = journey).order_by('-id')
    dominos = Domino.objects.filter(author=user.id, isPinned = False, assignedJourney = journey, isCompleted = False).order_by('-id')
    completeddominos = Domino.objects.filter(author=user.id, isPinned = False, assignedJourney = journey, isCompleted = True).order_by('-id')
    return render(request, 'journal/journey.html', {'user':user, 'dominos':dominos,'completeddominos':completeddominos, 'pinneddominos':pinneddominos, 'journeySelected': journeySelected, 'journey': journey, 'journeys': journeys})
    #return HttpResponse("hi")

def delete(request, delete_id):
    #Query Dominos
    user = request.user
    domino = Domino.objects.get(author=user.id,id = delete_id)
    #List Load
    domino.delete()
    if domino.parentId:
        redirecturl = '/domino/id/' + str(domino.parentId.id)
    else:
        redirecturl = '/domino'
    return redirect(redirecturl)
    #return HttpResponse("hi")


def deleteJourneyDomino(request, domino_id, journey_id):
    user = request.user
    domino = Domino.objects.get(author=user.id,id = domino_id)
    domino.delete()
    rediredturl = '/domino/journey/' + str(journey_id)
    return redirect(rediredturl)

def newjourney(request):
    if request.method == 'POST':
        user = request.user
        form = NewJourneyForm(request.POST)        
        if form.is_valid():   
            newjourney = form.save(commit=False)
            newjourney.author = user
            newjourney.save()
            return redirect('/domino')        
    else:        
        user = request.user
        form = NewJourneyForm(author=request.user)
        return render(request, 'journal/newjourney.html', {'user':user,"form":form})
        #return HttpResponse("hi")
        


#Update Journey
def updatejourney(request, journey_id):
    if request.method == 'POST':
        user = request.user
        journey = Collection.objects.get(author=user.id,id = journey_id)
        form = NewDominoForm(request.POST, instance = journey)
        if form.is_valid():   
            editjourney = form.save(commit=False)
            editjourney.author = user            
            editjourney.save()
            rediredturl = '/domino/journey/' + str(journey_id)
            return redirect(rediredturl)
    else:
        user = request.user
        journey = Collection.objects.get(author=user.id, id = domino_id)
        form = NewJourneyForm(instance = journey)        
        return render(request, 'domino/newjourney.html', {'user':user,"form":form})




def privacy(request):
    return render(request, 'journal/privacy.html')

def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/domino/login')

        
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})


def login(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect('/domino')
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})
