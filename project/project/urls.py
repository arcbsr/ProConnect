"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from logging import handlers
from django.contrib import admin
from django.urls import path, include
from sqlalchemy import null
from api import urls as api_urls
# without this line django admin doesn't get css, js files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.views import exception_handler
from http import HTTPStatus
from typing import Any
from response import ResponseSend
from rest_framework import status 
from rest_framework.views import Response

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = "django_404_project.views.page_not_found_view"
# without this line django admin doesn't get css, js files
urlpatterns += staticfiles_urlpatterns()


# https://www.youtube.com/watch?v=WUMEAZWM5xE
# youtube link to add more details....
def api_exception_handler(exc , context ) :

    """Custom API exception handler."""

    # handlers = {
    #     'ValidationError': _handler_generic_error,

    # }


    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    error_payload = ResponseSend.sendMsg('')
    if response is not None:
        # Using the description's of the HTTPStatus class as error message.

        # {
        #     "error": {
        #         "status_code": 0,
        #         "message": "",
        #         # "details": [],
        #     }
        # }
        http_code_to_message = {v.value: v.description for v in HTTPStatus}
        error = error_payload["error"]
        status_code = response.status_code

        # error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload
    else:
        error["details"] = 'Unknown'
    
    return response
  