from django.db import models
from django_extensions.db.fields import CreationDateTimeField,\
    ModificationDateTimeField

class Client(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    client = models.ForeignKey(Client, 
        related_name='project_task', on_delete=models.CASCADE,
        null=True, db_index = True
        )
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    project = models.ForeignKey(Project, 
        related_name='project_task',null=True, 
        on_delete=models.CASCADE, db_index = True
        )
    status = models.CharField(max_length=20, default='TODO')
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
