from django.db import models


# ============================================================
# SQL 注入漏洞场景 — 达梦 DM8 方言
# ============================================================

class SqliUser(models.Model):
    """用户表（达梦数据库）"""

    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码(MD5)')
    email = models.EmailField(verbose_name='邮箱')
    role = models.CharField(max_length=20, default='user', verbose_name='角色')

    class Meta:
        db_table = 'sqli_users'
        app_label = 'vulns'

    def __str__(self):
        return self.username


class SqliPost(models.Model):
    """文章表（达梦数据库）"""

    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.CharField(max_length=50, verbose_name='作者')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sqli_posts'
        app_label = 'vulns'

    def __str__(self):
        return self.title


# ============================================================
# XSS 漏洞场景
# ============================================================

class XssComment(models.Model):
    """评论表"""

    username = models.CharField(max_length=50)
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xss_comments'
        app_label = 'vulns'

    def __str__(self):
        return f"{self.username}: {self.content[:30]}"


# ============================================================
# 文件上传漏洞场景
# ============================================================

class UploadedFile(models.Model):
    """上传文件表"""

    filename = models.CharField(max_length=255, verbose_name='文件名')
    filepath = models.CharField(max_length=500, verbose_name='存储路径')
    uploader = models.CharField(max_length=50, verbose_name='上传者')
    size = models.IntegerField(verbose_name='文件大小(字节)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upload_files'
        app_label = 'vulns'

    def __str__(self):
        return self.filename


# ============================================================
# 命令注入漏洞场景
# ============================================================

class PingResult(models.Model):
    """ping 结果记录"""

    target = models.CharField(max_length=200, verbose_name='目标地址')
    result = models.TextField(verbose_name='执行结果')
    executed_by = models.CharField(max_length=50, verbose_name='执行者')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cmd_results'
        app_label = 'vulns'

    def __str__(self):
        return f"Ping {self.target}"
