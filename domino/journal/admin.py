from django.contrib import admin
#import models
from .models import Domino, List, Collection, Note, Type, TimeBlock

# Register your models here.
admin.site.register(Collection)
admin.site.register(Domino)
admin.site.register(List)
admin.site.register(Note)
admin.site.register(Type)
admin.site.register(TimeBlock)
