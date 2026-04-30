# ============================================================
# XinRange App Dockerfile
# 基础镜像: Python 3.11
# ============================================================

FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Python 依赖
# dmPython: 达梦官方驱动（开发阶段可选，USE_SQLITE_DEV=True 时不需要）
# 如需连接达梦，将 dm_python-*-cp311-cp311*.whl 放入根目录
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# 尝试安装达梦驱动（如果本地有 .whl 文件则安装，否则跳过）
COPY *.whl /tmp/dm_wheel/ 2>/dev/null || true
RUN pip install --no-cache-dir /tmp/dm_wheel/*.whl 2>/dev/null || true

# 复制应用代码
COPY app/ ./app/
COPY config/ ./config/
COPY manage.py ./

# 收集静态文件
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
