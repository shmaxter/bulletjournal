from django.urls import path, include
from . import views

urlpatterns=[
    path('/', views.index, name="index"),
    path('/new', views.new, name="new"),
    path('/new/j/<int:journey_id>/', views.newJourneyDomino, name="newJourneyDomino"),
    path('/newjourney', views.newjourney, name="newjourney"),
    path('/updatejourney/<int:journey_id>', views.updatejourney, name="updatejourney"),
    path('/journey/<int:journey_id>', views.journey, name="journey"),
    path('/delete/<int:delete_id>', views.delete, name="delete"),
    path('/delete/j/<int:journey_id>/f/<int:domino_id>/', views.deleteJourneyDomino, name='deleteJourneyDomino'),
    path('/id/<int:domino_id>/', views.domino, name='domino'),
    path('/new/<int:domino_id>/', views.newsub, name='newsub'),
    path('/pin/<int:domino_id>/', views.pin, name='pin'),
    path('/pin/p/<int:domino_id>/', views.pinParent, name='pinParent'),
    path('/pin/h/<int:domino_id>/', views.pinHome, name='pinHome'),
    path('/pin/j/<int:journey_id>/f/<int:domino_id>/', views.pinJourney, name='pinJourney'),
    path('/complete/<int:domino_id>/', views.complete, name='complete'),
    path('/complete/p/<int:domino_id>/', views.completeParent, name='completeParent'),
    path('/complete/j/<int:journey_id>/f/<int:domino_id>/', views.completeJourney, name='completeJourney'),
    path('/complete/h/<int:domino_id>/', views.completeHome, name='completeHome'),
    path('/note/<int:domino_id>/', views.newnote, name='newnote'),
    path('/time/<int:domino_id>/', views.newtime, name='newtime'),
    path('/edit/<int:domino_id>/', views.update, name='update'),
    path('/privacy-policy', views.privacy, name="privacy"),
    path('/register', views.register, name="register"),
    #path('/login', views.login, name="login"),  
    path('/', include("django.contrib.auth.urls"))  
]
