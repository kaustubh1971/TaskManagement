from datetime import date
import json


from django.db.models import F
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.db import transaction

# Create your views here.
from .models import Task, Project, Client
from .utils import required_field_difference,extra_fields_response, \
    missing_fields_response, JSONResponse
from .error_messages import Message
from .serializer import ProjectDetailSerializer


@api_view(["GET"])
def get_all_tasks(request):
    try:
        data = request.GET
        page_number = data.get("page_number") or None
        page_size = data.get("page_size") or None
        if page_number and page_size:
            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(7).format("data provided")
                    })
        lower_limit, upper_limit = None, None
        if page_size and page_number:
            range_val = [x*page_size for x in range(page_number+1)]
            lower_limit = range_val[page_number-1]
            upper_limit = lower_limit + page_size
        task_details = Task.objects.annotate(
            project_name=F('project__name'),
            client_name=F('project__client__name')
        ).values(
            "id","name","description","status",
            "project_name","client_name"
        )
        if str(lower_limit).isnumeric() and \
            str(upper_limit).isnumeric():
            task_details = task_details[lower_limit:upper_limit]
            if not task_details:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(6).format(page_number)
                    })

        return JSONResponse({
            'code': 1,
            'response': task_details,
            'message': Message.code(101)
            })

    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })


@api_view(["POST"])
def create_new_task(request):
    try:
        required_fields = [
            'task_name', 'description',
            'project_name', 'client_name'
        ]
        optional_fields = ['status']
        # convert unicode to normal string
        post_params_key = map(str, request.data.keys())
        required, not_needed = required_field_difference(
            required_fields,
            optional_fields,
            post_params_key)
        # if extra fields is provided
        if not_needed:
            return extra_fields_response(not_needed)
        # if required field not provided
        if required:
            return missing_fields_response(required)
        data = request.data
        task_name = data.get('task_name')
        description = data.get('description')
        project_name = data.get('project_name') 
        client_name = data.get('client_name')
        client_exists = False
        project_exists = False
        project_name = project_name.strip().upper()
        client_name = client_name.strip().upper()
        try:
            existing_client = Client.objects.get(
                name = client_name
            )
            if existing_client:
                client_exists = True
                project_list = existing_client.project_task.values_list(
                    "name", flat=True
                )
                if project_name in project_list:
                    project_exists = True
        except:
            pass
        
        status = data.get('status')
        if status:
            status = status.upper()
            if status not in ["TODO", "WIP", "ONHOLD", "DONE"]:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(2)
                    })

        with transaction.atomic():
            
            if not project_exists:
                if client_exists:
                    client_object = existing_client
                else:
                    client_object = Client.objects.create(
                        name = client_name
                    )

                project_object = Project.objects.create(
                    name = project_name,
                    client = client_object
                )
                project_object.start_date = date.today()
                project_object.save()
            else:
                project_object = Project.objects.get(
                    client__name=client_name,
                    name=project_name
                )
                    
            task_object = Task.objects.create(
                name=task_name,
                description=description,
                project = project_object
            )
            if status:
                task_object.status = status
                task_object.save()
            return JSONResponse({
                'code': 1,
                'response': {},
                'message': Message.code(103)
                })
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })


@api_view(["DELETE"])
def delete_task(request):
    try:
        data = request.data
        task_id = data.get('task_id')
        if not task_id:
            return missing_fields_response("task_id")
        try:
            task_object = Task.objects.get(
                id = task_id
            )
        except:
            return JSONResponse({
                'code': 0, 
                'response': {}, 
                'message': Message.code(1).format('task_id')
                })   
        task_object.delete()
        return JSONResponse({
            'code': 1,
            'response': {},
            'message': Message.code(104)
            })
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })


@api_view(["PUT"])
def update_task_status(request):
    try:
        data = request.data
        required_fields = [
            'task_id', 'status'
        ]
        optional_fields = []
        # convert unicode to normal string
        post_params_key = map(str, request.data.keys())
        required, not_needed = required_field_difference(
            required_fields,
            optional_fields,
            post_params_key)
        # if extra fields is provided
        if not_needed:
            return extra_fields_response(not_needed)
        # if required field not provided
        if required:
            return missing_fields_response(required)
        task_id = data.get('task_id') 
        status = data.get('status')
        try:
            task_object = Task.objects.get(
                id=task_id
            )
        except:
            return JSONResponse({
                'code': 0, 
                'response': {}, 
                'message': Message.code(1).format('task_id')
                })   
        if status not in ["TODO", "WIP", "ONHOLD", "DONE"]:
            return JSONResponse({
                'code': 0, 
                'response': {}, 
                'message': Message.code(2)
                })   

        task_object.status = status
        task_object.save()
        return JSONResponse({
            'code': 1,
            'response': {},
            'message': Message.code(102)
            })
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })


@api_view(["GET"])
def get_all_projects(request):
    try:
        data = request.GET
        page_number = data.get("page_number") or None
        page_size = data.get("page_size") or None
        lower_limit, upper_limit = None, None
        if page_size and page_number:
            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(7).format("data provided")
                    })
            range_val = [x*page_size for x in range(page_number+1)]
            lower_limit = range_val[page_number-1]
            upper_limit = lower_limit + page_size
        project_details = Project.objects.filter(
            end_date__isnull=True
        ).annotate(
                client_name=F('client__name')
            ).values(
                "id","name","description",
                "start_date","end_date","client_name"        
            ).order_by("created_date")

        if str(lower_limit).isnumeric() and \
            str(upper_limit).isnumeric():
            project_details = project_details[lower_limit:upper_limit]
            if not project_details:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(6).format(page_number)
                    })
        return JSONResponse({
            'code': 1,
            'response': project_details,
            'message': Message.code(101)
            })

    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })



@api_view(["POST"])
def create_new_project(request):
    """ 
    Content-Type = application/json

    pass such data in body

    Eg: 

    {
    'description':'payment integration', 
    'project_name':'PAYMENT GATEWAY2', 
    'client_name':'SBI',
    'task_list':[
        {
            "name":"get payment",
            "description":"get payment from user",
            "status":"TODO",
        },
        {   
            "name":"",
            "description":"work",
            "status":"WIP",
        },
        {
            "name":"update payment status",
            "description":"after receiving payment update data in system",
            "status":"ONHOLD"
        },
    ]
    }
    """
    try:
        required_fields = [
            'description', 'project_name', 'client_name'
        ]
        optional_fields = ['task_list']
        data = request.body.decode("utf-8")
        import ast
        data = ast.literal_eval(data)
        # convert unicode to normal string
        post_params_key = map(str, data.keys())
        required, not_needed = required_field_difference(
            required_fields,
            optional_fields,
            post_params_key)
        # if extra fields is provided
        if not_needed:
            return extra_fields_response(not_needed)
        # if required field not provided
        if required:
            return missing_fields_response(required)
        # data = request.data
        # email = data.get('email')
        project_name = data.get('project_name').strip().upper()
        description = data.get('description').strip().upper()
        client_name = data.get('client_name').strip().upper()
        client_exists = False
        project_exists = False
        try:
            existing_client = Client.objects.get(
                name = client_name
            )
            if existing_client:
                client_exists = True
                project_list = existing_client.project_task.values_list(
                    "name", flat=True
                )
                if project_name in project_list:
                    project_exists = True
        except:
            pass
        if project_exists:
            error_msg = Message.code(3).format(project_name,client_name)
            return JSONResponse({
                'code': 0,
                'response': {},
                'message': error_msg
                })

        with transaction.atomic():
            if client_exists:
                client_object = existing_client
            else:
                client_object = Client.objects.create(
                    name = client_name
                )
            project_object = Project.objects.create(
                name = project_name,
                start_date = date.today()
            )
            project_object.client = client_object
            project_object.save()
            task_list = data.get('task_list')
            task_data = []
            if task_list:
                for task_info in task_list:  
                    task_name = task_info.get('name') if \
                        task_info.get('name') else None
                    
                    if not task_name:
                        continue

                    description = task_info.get('description') if \
                        task_info.get('description') else None

                    status = task_info.get('status') if \
                        task_info.get('status') else 'TODO'

                    if status not in ["TODO", "WIP", "ONHOLD", "DONE"]:
                        continue

                    tasks = Task(
                        name=task_name,
                        project=project_object,
                        description=description,
                        status=status
                    )
                    task_data.append(tasks)

            if len(task_data)>0:
                Task.objects.bulk_create(task_data)
            return JSONResponse({
                'code': 1,
                'response': {},
                'message': Message.code(103)
                })
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })


@api_view(["DELETE"])
def delete_project(request):
    try:
        data = request.data
        project_id = data.get('project_id')
        if not project_id:
            return missing_fields_response("project_id")
        try:
            project_object = Project.objects.get(
                id = project_id
            )
        except:
            return JSONResponse({
                'code': 0, 
                'response': {}, 
                'message': Message.code(1).format('project_id')
                })   
        project_object.delete()
        return JSONResponse({
            'code': 1,
            'response': {},
            'message': Message.code(104)
            })

    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })


@api_view(["GET"])
def get_project_detail(request):
    try:
        project_id = request.GET.get('project_id')
        if not project_id:
            return missing_fields_response("project_id")
        try:
            project_object = Project.objects.get(
                id = project_id
            )
        except:
            return JSONResponse({
                'code': 0, 
                'response': {}, 
                'message': Message.code(1).format("project_id")
                })
        project_details = ProjectDetailSerializer(
				project_object)
        return JSONResponse(
				{
                    'code': 1,
					'response': {"project_details": project_details.data},
					'message': Message.code(101)
				}
			)
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': e
            })