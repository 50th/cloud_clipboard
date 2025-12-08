from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

from .response_codes import RESPONSE_CODES


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    """
    response = exception_handler(exc, context)
    print(response)
    if response is not None:
        response.data["code"] = response.status_code
        response.data["message"] = RESPONSE_CODES[response.status_code]
        response.data["data"] = {}
        return Response(response.status_code, status=response.status_code)
    # 未处理异常（500）
    return Response(500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
