from django.contrib import admin
from .models import Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    raw_id_fields = ['project',]
    list_display = ('id', 'name', 'description', 'status','updated_date', 'created_date')
    #list_filter = ('step', 'status', 'action')
    search_fields = ('id', 'name', 'status')
admin.site.register(Task, TaskAdmin)