from rest_framework import serializers
from .models import Project


class ProjectDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    client_name = serializers.SerializerMethodField()
    task_list = serializers.SerializerMethodField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def get_client_name(self, instance):
        return instance.client.name

    def get_task_list(self, instance):
        return instance.project_task.values(
            "name", "description", "status"
            )

    class Meta:
        model = Project
        fields = ['name', 'description', 'client_name','start_date', 
                  'end_date', 'task_list']