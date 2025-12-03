import logging

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .models import Clipboard, ClipboardFile
from .serializers import ClipboardSerializer

logger = logging.getLogger(__name__)


class ClipboardViewSet(viewsets.ModelViewSet):
    serializer_class = ClipboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Clipboard.objects.filter(user=self.request.user)
        permission = self.request.query_params.get("permission", None)
        logger.info("permission: %s", permission)
        if permission:
            queryset = queryset.filter(permission=permission)
        return queryset

    def perform_create(self, serializer):
        logger.info("create clipboard")
        clipboard = serializer.save(user=self.request.user, last_modified_by=self.request.user)
        # 处理上传的文件
        logger.info("create clipboard files: %s", self.request.FILES)
        if "file_content" in self.request.FILES:
            ClipboardFile.objects.create(
                clipboard=clipboard,
                file_content=self.request.FILES["file_content"],
                uploaded_by=self.request.user,
            )
        elif "file_contents" in self.request.FILES:
            for file_content in self.request.FILES.getlist("file_contents"):
                ClipboardFile.objects.create(
                    clipboard=clipboard,
                    file_content=file_content,
                    uploaded_by=self.request.user,
                )
