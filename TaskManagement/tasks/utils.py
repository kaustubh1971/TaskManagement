from .error_messages import Message

# from __future__ import division
from rest_framework.renderers import JSONRenderer
from django.http.response import HttpResponse

    
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def missing_fields_response(list_of_missing_fields):
    if len(list_of_missing_fields) == 1:
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} field is {}".format(
            list_of_missing_fields[0], Message.code(4))})
    else:
        missing_fields = ", ".join(list_of_missing_fields)
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} fields are {}".format(
            missing_fields, Message.code(4))})


def extra_fields_response(list_of_extra_fields):
    if len(list_of_extra_fields) == 1:
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} field is {}".format(
            list_of_extra_fields[0], Message.code(5))})
    else:
        extra_fields = ", ".join(list_of_extra_fields)
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} fields are {}".format(
            extra_fields, Message.code(5))})


def required_field_difference(required_field, optional_fields, parameters):
    required_field_set = set(required_field)
    optional_fields_set = set(optional_fields)
    parameters_set = set(parameters)
    required = required_field_set.difference(parameters_set)
    not_needed = parameters_set.difference(required_field_set).difference(optional_fields_set)
    return list(required), list(not_needed)