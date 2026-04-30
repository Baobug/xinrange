"""
XinRange 漏洞场景视图
每个漏洞模块按 Low / Medium / High 三级难度实现。
⚠️ 这些代码仅用于合法安全教学，切勿用于未授权系统。
"""

import os
import subprocess
import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import connection, connections
from django.db.models import Q
from django.conf import settings
from .models import SqliPost, SqliUser, XssComment, UploadedFile, PingResult

# 开发模式：优先尝试达梦，失败则降级 SQLite
USE_SQLITE_DEV = os.getenv('USE_SQLITE_DEV', 'False').lower() == 'true'


def _get_db_alias():
    """获取当前数据库别名（达梦优先，失败降级 SQLite）"""
    if USE_SQLITE_DEV:
        return 'default'
    try:
        conn = connections['dameng']
        conn.ensure_connection()
        return 'dameng'
    except Exception:
        return 'default'


# ============================================================
# SQL 注入模块
# ============================================================

def sqli_home(request):
    """SQL 注入主页"""
    difficulty = request.GET.get('level', 'low')
    return render(request, 'vulns/sqli/home.html', {'difficulty': difficulty})


@require_http_methods(["GET", "POST"])
def sqli_search(request):
    """
    SQL 注入漏洞演示
    Low:  直接拼接用户输入，无任何过滤
    Medium: 简单过滤但仍可绕过
    High:  参数化查询（安全示例）
    """
    difficulty = request.GET.get('level', 'low')
    results = []
    raw_sql = None
    query = request.GET.get('q', '')

    if query:
        db_alias = _get_db_alias()

        if difficulty in ['low', 'medium']:
            # ❌ Low/Medium: 直接拼接（SQL 注入演示）
            if db_alias == 'dameng':
                # 达梦 DM8 语法
                raw_sql = f"SELECT * FROM sqli_posts WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
            else:
                # SQLite 语法（开发模式）
                raw_sql = f"SELECT * FROM sqli_posts WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"

            with connection.cursor(db_alias) as cursor:
                cursor.execute(raw_sql)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]

        else:
            # ✅ High: Django ORM 参数化查询（兼容 SQLite / 达梦）
            results = [
                {'id': p.id, 'title': p.title, 'content': p.content, 'author': p.author}
                for p in SqliPost.objects.using(db_alias).filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
            ]
            raw_sql = None

    return render(request, 'vulns/sqli/search.html', {
        'results': results,
        'query': query,
        'difficulty': difficulty,
        'raw_sql': raw_sql,
    })


@require_http_methods(["GET", "POST"])
def sqli_login(request):
    """
    SQL 注入登录绕过
    Low: 直接拼接，可 bypass
    Medium: 过滤空格，但可绕过
    High: 参数化 + 哈希
    """
    difficulty = request.GET.get('level', 'low')
    error = None
    db_alias = _get_db_alias()

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if difficulty == 'low':
            sql = f"SELECT * FROM sqli_users WHERE username='{username}' AND password='{password}'"
            with connection.cursor(db_alias) as cursor:
                cursor.execute(sql)
                user = cursor.fetchone()

        elif difficulty == 'medium':
            username_clean = username.replace(' ', '').replace('--', '').replace('#', '')
            sql = f"SELECT * FROM sqli_users WHERE username='{username_clean}' AND password='{password}'"
            with connection.cursor(db_alias) as cursor:
                cursor.execute(sql)
                user = cursor.fetchone()

        else:
            pwd_hash = hashlib.md5(password.encode()).hexdigest()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM sqli_users WHERE username=%s AND password=%s",
                    [username, pwd_hash]
                )
                user = cursor.fetchone()

        if user:
            return HttpResponse(f"<div class='alert alert-success'>登录成功: {user[1]} (角色: {user[4] if len(user) > 4 else 'user'})</div>")
        else:
            error = "用户名或密码错误"

    return render(request, 'vulns/sqli/login.html', {'difficulty': difficulty, 'error': error})


# ============================================================
# XSS 跨站脚本模块
# ============================================================

def xss_home(request):
    """XSS 主页"""
    difficulty = request.GET.get('level', 'low')
    db_alias = _get_db_alias()
    try:
        comments = XssComment.objects.using(db_alias).all()[:20]
    except Exception:
        comments = []
    return render(request, 'vulns/xss/home.html', {
        'difficulty': difficulty,
        'comments': comments,
    })


@require_http_methods(["POST"])
def xss_post(request):
    """XSS 漏洞评论提交"""
    difficulty = request.GET.get('level', 'low')
    username = request.POST.get('username', '')
    content = request.POST.get('content', '')
    db_alias = _get_db_alias()

    if difficulty in ['low', 'medium']:
        XssComment.objects.using(db_alias).create(username=username, content=content)
    else:
        import html
        XssComment.objects.using(db_alias).create(
            username=html.escape(username),
            content=html.escape(content),
        )

    return redirect(f'/vulns/xss/?level={difficulty}')


# ============================================================
# 文件上传漏洞模块
# ============================================================

def upload_home(request):
    """文件上传主页"""
    difficulty = request.GET.get('level', 'low')
    db_alias = _get_db_alias()
    try:
        files = UploadedFile.objects.using(db_alias).all()[:20]
    except Exception:
        files = []
    return render(request, 'vulns/upload/home.html', {
        'difficulty': difficulty,
        'files': files,
    })


@require_http_methods(["POST"])
def upload_do(request):
    """文件上传处理"""
    difficulty = request.GET.get('level', 'low')
    uploaded_file = request.FILES.get('file')
    uploader = request.POST.get('uploader', 'anonymous')
    db_alias = _get_db_alias()

    if not uploaded_file:
        return HttpResponse("请选择文件", status=400)

    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()

    upload_dir = '/tmp/xinrange/uploads'
    os.makedirs(upload_dir, exist_ok=True)

    if difficulty == 'low':
        save_path = os.path.join(upload_dir, filename)

    elif difficulty == 'medium':
        blacklist = ['.php', '.jsp', '.asp', '.aspx']
        if ext in blacklist:
            return HttpResponse(f"禁止上传 {ext} 文件", status=403)
        save_path = os.path.join(upload_dir, filename)

    else:
        whitelist = ['.jpg', '.png', '.gif', '.pdf', '.txt']
        if ext not in whitelist:
            return HttpResponse(f"仅允许 {whitelist} 格式", status=403)
        import uuid
        safe_name = f"{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(upload_dir, safe_name)

    with open(save_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    UploadedFile.objects.using(db_alias).create(
        filename=filename,
        filepath=save_path,
        uploader=uploader,
        size=uploaded_file.size,
    )

    return HttpResponse(f"上传成功: {filename}")


# ============================================================
# 命令注入漏洞模块
# ============================================================

def cmd_home(request):
    """命令注入主页"""
    difficulty = request.GET.get('level', 'low')
    db_alias = _get_db_alias()
    try:
        results = PingResult.objects.using(db_alias).all()[:20]
    except Exception:
        results = []
    return render(request, 'vulns/cmd/home.html', {
        'difficulty': difficulty,
        'results': results,
    })


@require_http_methods(["POST"])
def cmd_ping(request):
    """Ping 命令执行（命令注入演示）"""
    difficulty = request.GET.get('level', 'low')
    target = request.POST.get('target', '')
    executed_by = request.POST.get('executed_by', 'guest')
    db_alias = _get_db_alias()
    result = ''

    if not target:
        return HttpResponse("请输入目标地址", status=400)

    if difficulty == 'low':
        cmd = f"ping -c 3 {target}"
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10).decode()

    elif difficulty == 'medium':
        dangerous = [';', '|', '&', '`', '$', '(', ')']
        blocked = next((c for c in dangerous if c in target), None)
        if blocked:
            return HttpResponse(f"检测到非法字符: {blocked}", status=400)
        cmd = f"ping -c 3 {target}"
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10).decode()

    else:
        target_clean = ''.join(c for c in target if c.isalnum() or c in ['.', '-', '_'])
        result = subprocess.check_output(['ping', '-c', '3', target_clean], timeout=10).decode()

    PingResult.objects.using(db_alias).create(
        target=target,
        result=result[:500],
        executed_by=executed_by,
    )

    return HttpResponse(f"<pre>{result}</pre>")
