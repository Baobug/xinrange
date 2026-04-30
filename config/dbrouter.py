"""
达梦数据库路由
- 核心数据（用户、积分）: SQLite
- 靶场漏洞数据: 达梦 DM8
"""


class DamengRouter:
    """
    控制模型指向哪个数据库。
    靶场漏洞相关表走达梦，核心系统表走默认 SQLite。
    """

    # 走达梦的 app_label
    DAMENG_APPS = {'vulns'}
    # 走达梦的表名模式（靶场漏洞场景表）
    DAMENG_TABLES = {
        'sqli_users', 'sqli_posts', 'sqli_comments',
        'xss_guestbook', 'xss_comments',
        'upload_files', 'cmd_results',
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.DAMENG_APPS:
            return 'dameng'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.DAMENG_APPS:
            return 'dameng'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # 同库关联允许
        if obj1._meta.app_label in self.DAMENG_APPS:
            return obj2._meta.app_label in self.DAMENG_APPS
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.DAMENG_APPS:
            return db == 'dameng'
        return db == 'default'
