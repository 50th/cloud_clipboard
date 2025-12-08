from rest_framework import status
from rest_framework.response import Response


RESPONSE_CODES = {
    0: "Success",
}


class CustomResponse(Response):
    """自定义响应类，统一返回格式"""

    def __init__(
        self,
        code=0,
        message=RESPONSE_CODES[0],
        data=None,
        status=status.HTTP_200_OK,
        **kwargs
    ):
        response_data = {
            "code": code,
            "message": message,
            "data": {},
        }

        if data is not None:
            response_data["data"] = data

        super().__init__(response_data, status=status, **kwargs)
