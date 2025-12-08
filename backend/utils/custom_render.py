from rest_framework import renderers

from .response_codes import RESPONSE_CODES


class CustomRender(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        print(data)
        print(renderer_context)
        if isinstance(data, int):
            response_data = {
                "code": data,
                "message": RESPONSE_CODES[data],
                "data": {},
            }
        elif isinstance(data, tuple):
            if len(data) == 2:
                response_data = {
                    "code": data[0],
                    "message": RESPONSE_CODES[data[0]],
                    "data": data[1],
                }
            elif len(data) == 3:
                response_data = {
                    "code": data[0],
                    "message": data[1],
                    "data": data[2],
                }
        else:
            response_data = {
                "code": 0,
                "message": RESPONSE_CODES[0],
                "data": data,
            }
        return super().render(response_data, accepted_media_type, renderer_context)
