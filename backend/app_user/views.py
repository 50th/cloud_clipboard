import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer
from constants.response_codes import ResponseCodes

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            logger.info("UserLoginView validate fail: %s", e)
            return Response(ResponseCodes.USERNAME_OR_PASSWORD_ERROR, status=status.HTTP_200_OK)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
