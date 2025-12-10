from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Clipboard, ClipboardFile, ClipboardPermission


class ClipboardFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def get_file_url(self, obj):
        # 生成文件访问URL
        if obj.file_content and obj.file_content.url:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file_content.url)
            return obj.file_content.url
        return None

    class Meta:
        model = ClipboardFile
        fields = (
            "id",
            "file_content",
            "file_name",
            "file_size",
            "uploaded_by",
            "created_at",
            "file_url",
        )
        read_only_fields = (
            "id",
            "file_name",
            "file_size",
            "uploaded_by",
            "created_at",
            "file_url",
        )


class ClipboardListSerializer(serializers.ModelSerializer):
    permission = serializers.ChoiceField(
        choices=ClipboardPermission.choices,
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    permission_display = serializers.ReadOnlyField(source="get_permission_display", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_user = serializers.ReadOnlyField(source='user.username', read_only=True)
    last_modified_user = serializers.ReadOnlyField(source='last_modified_by.username', read_only=True)

    class Meta:
        model = Clipboard
        fields = (
            "id",
            "title",
            "description",
            "permission",
            "permission_display",
            "share_id",
            "expired_at",
            "created_at",
            "updated_at",
            "created_user",
            "last_modified_user",
        )


class ClipboardSerializer(ClipboardListSerializer):
    share_password = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Clipboard
        fields = (
            "id",
            "title",
            "text_content",
            "description",
            "permission",
            "share_id",
            "share_password",
            "expired_at",
            "created_at",
            "updated_at",
            "created_user",
            "last_modified_user",
        )
        read_only_fields = (
            "id",
            "share_id",
            "created_at",
            "updated_at",
            "created_user",
            "last_modified_user",
        )

    def validate(self, attrs):
        permission = attrs["permission"]
        share_password = attrs.get("share_password")

        if permission == ClipboardPermission.SHARED_PASSWORD and not share_password:
            raise serializers.ValidationError(
                {"share_password": "带密码共享时，密码不能为空"}
            )
        if (
            permission is not None
            and permission != ClipboardPermission.SHARED_PASSWORD
            and share_password
        ):
            raise serializers.ValidationError(
                {"share_password": "只有带密码共享类型才能设置密码"}
            )
        return attrs

    def create(self, validated_data):
        if validated_data["permission"] != ClipboardPermission.SHARED_PASSWORD and validated_data.get("share_password"):
            validated_data["share_password"] = None
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if instance.permission != validated_data["permission"]:
            pass
        if validated_data["permission"] != ClipboardPermission.SHARED_PASSWORD and validated_data.get("share_password"):
            validated_data["share_password"] = None
        return super().update(instance, validated_data)
