from django.db import models
from django.contrib.auth.models import User


def get_clipboard_file_path(instance: models.FileField, filename):
    """生成剪贴板文件的保存路径。
    
    为了确保文件名唯一，使用UUID生成新的文件名，并按照剪贴板ID进行目录组织。
    
    Args:
        instance: ClipboardFile实例
        filename: 原始文件名
        
    Returns:
        str: 生成的文件保存路径
    """
    # 使用UUID确保文件名唯一
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    # 使用剪贴板ID作为目录名
    return os.path.join('clipboard_files', str(instance.clipboard.id), filename)



# 剪贴板权限枚举
class ClipboardPermission(model.TextChoices):
    PRIVATE = 'private', '私人'
    PUBLISH = 'publish', '公开'
    SHARED_PASSWORD = 'shared_password', '带密码共享'


# 剪切板文件模型
class ClipboardFile(models.Model):
    """剪切板文件模型

    一个剪贴板可以关联多个文件，通过外键与Clipboard模型关联。

    Attribute:
        clipboard: 关联的剪贴板对象
        uploaded_by: 上传文件的用户
        file_content: 文件内容存储
        file_name: 文件名
        file_size: 文件大小（字节）
        created_at: 创建时间
    """
    clipboard = models.ForeignKey(
        Clipboard,
        on_delete=models.CASCADE,
        related_name='files',
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_files',
    )
    file_content = models.FileField(upload_to=get_clipboard_file_path)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File {self.id} - {self.file_name} (Clipboard: {self.clipboard.id})'

    def save(self, *args, **kwargs):
        """保存文件时自动更新文件名和大小。

        当文件内容被修改时，自动从文件对象中获取文件名和大小。
        """
        if self.file_content:
            self.file_name = self.file_content.name
            self.file_size = self.file_content.size
        super().save(*args, **kwargs)


# 剪贴板模型
class Clipboard(models.Model):
    """剪切板模型，存储用户剪切板内容，包括文本和文件。

    一个剪贴板可以同时包含文本内容和多个文件，支持多种权限设置和共享功能。

    Attributes:
        user: 剪贴板的所有者
        title: 剪贴板标题
        description: 剪贴板描述
        text_content: 文本内容
        permission: 权限设置（私人、公开、带密码共享）
        share_password: 共享密码（哈希存储）
        share_id: 唯一共享标识符
        created_at: 创建时间
        updated_at: 更新时间
        expires_at: 过期时间（可空）
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clipboards',
    )
    title = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # 文本内容
    text_content = models.TextField(blank=True, null=True)
    # 权限控制
    permission = models.CharField(
        max_length=20,
        choices=ClipboardPermission,
        default=ClipboardPermission.PRIVATE,
    )
    # 共享信息
    shared_password = models.CharField(max_length=64, blank=True, null=True)
    shared_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_clipboards',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Clipboard {self.id} - {self.title or "Untitled"}'
