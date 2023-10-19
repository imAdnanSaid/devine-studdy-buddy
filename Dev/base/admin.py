from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Topic, Message, User

# Register your models here.


admin.site.register(Room)
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Message)