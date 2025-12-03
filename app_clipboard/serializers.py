from rest_framework import serializers

from .models import Clipboard, ClipboardFile, ClipboardPermission


# class UserProfileSerializer(serializers.ModelSerializer):
#     """Serializer for user profile objects"""

#     class Meta:
#         model = UserProfile
#         fields = ("id", "name", "email", "password")
#         extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

#     def create(self, validated_data):
#         """Create a new user profile"""
#         user = UserProfile.objects.create_user(
#             email=validated_data["email"],
#         )


class ClipboardFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

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


class ClipboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clipboard
        fields = (
            "id",
            "title",
            "text_content",
            "description",
            "permission",
            "shared_id",
            "shared_password",
            "expired_at",
            "created_at",
            "updated_at",
            "last_modified_by",
            "user",
        )
        read_only_fields = (
            "id",
            "shared_id",
            "created_at",
            "user",
            "last_modified_by",
        )
