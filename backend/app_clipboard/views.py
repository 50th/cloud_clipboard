import logging

from django.db.models import Q
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from constants.response_codes import ResponseCodes
from .models import Clipboard, ClipboardFile, ClipboardPermission
from .serializers import ClipboardSerializer, ClipboardListSerializer
from .permissions import HasClipboardPermission

logger = logging.getLogger(__name__)


class ClipboardViewSet(viewsets.ModelViewSet):
    serializer_class = ClipboardSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            queryset = Clipboard.objects.filter(user=self.request.user)
        else:
            queryset = Clipboard.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ClipboardListSerializer
        return ClipboardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, last_modified_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        获取剪切板，支持主键或 share id 查询
        """
        clipboard_id = kwargs.get('pk')

        if clipboard_id.isnumeric():
            instance = Clipboard.objects.filter(id=clipboard_id).first()
        else:
            instance = Clipboard.objects.filter(share_id=clipboard_id).first()
        if not instance:
            return Response(ResponseCodes.CLIPBOARD_NOT_EXIST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            instance = self.get_object()
        except Http404:
            return Response(ResponseCodes.CLIPBOARD_NOT_EXIST)

        if instance.user != self.request.user:
            return Response(ResponseCodes.PERMISSION_DENIED)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.permission != serializer.validated_data["permission"] and instance.user != self.request.user:
            return Response(ResponseCodes.PERMISSION_DENIED)
        serializer.validated_data["last_modified_by"] = request.user
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(ResponseCodes.CLIPBOARD_NOT_EXIST)
        if instance.user != self.request.user:
            return Response(ResponseCodes.PERMISSION_DENIED)
        self.perform_destroy(instance)
        return Response(ResponseCodes.OK)
