from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotFound):
        custom_response_data = {'error': 'Resource not found'}
        if response is not None:
            response.data = custom_response_data
            response.status_code = 404
        else:
            response = Response(custom_response_data, status=404)

    return response