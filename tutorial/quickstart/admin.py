from django.contrib import admin
from .models import StudentModel,Singer,Song

class StudentAdmin(admin.ModelAdmin):
    list_display=['id','name','roll','city']

admin.site.register(StudentModel,StudentAdmin)

@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display=['id','name','gender']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display=['id','title','singer','duration']

