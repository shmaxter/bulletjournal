from django.urls import path, include
from . import views

urlpatterns=[
    path('/', views.index, name="index"),
    path('/new', views.new, name="new"),
    path('/newjourney', views.newjourney, name="newjourney"),
    path('/calendar', views.calendar, name="calendar"),
    path('/updatejourney/<int:journey_id>', views.updatejourney, name="updatejourney"),
    path('/journey/<int:journey_id>', views.journey, name="journey"),
    path('/delete/<int:delete_id>', views.delete, name="delete"),
    path('/id/<int:domino_id>/', views.domino, name='domino'),
    path('/new/<int:domino_id>/', views.newsub, name='newsub'),
    path('/pin/<int:domino_id>/', views.pin, name='pin'),
    path('/pin/p/<int:domino_id>/', views.pinParent, name='pinParent'),
    path('/pin/h/<int:domino_id>/', views.pinHome, name='pinHome'),
    path('/complete/<int:domino_id>/', views.complete, name='complete'),
    path('/complete/p/<int:domino_id>/', views.completeParent, name='completeParent'),
    path('/complete/h/<int:domino_id>/', views.completeHome, name='completeHome'),
    path('/listitem/<int:list_id>/', views.listitem, name='listitem'),
    path('/list/<int:domino_id>/', views.newlist, name='newlist'),
    path('/note/<int:domino_id>/', views.newnote, name='newnote'),
    path('/time/<int:domino_id>/', views.newtime, name='newtime'),
    path('/edit/<int:domino_id>/', views.update, name='update'),
    path('/privacy-policy', views.privacy, name="privacy"),
    path('/register', views.register, name="register"),
    #path('/login', views.login, name="login"),  
    path('/', include("django.contrib.auth.urls"))  
]
