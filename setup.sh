#!/usr/bin/env bash
# ============================================================
# XinRange 环境准备脚本
# 运行平台：Windows Docker Desktop (WSL2)
# 用途：准备 DM8 镜像 + 启动靶场
# ============================================================
set -e

echo "============================================"
echo "  XinRange 环境准备脚本"
echo "  达梦 DM8 + 麒麟环境靶场"
echo "============================================"

# ---- 检查 Docker ----
if ! command -v docker &> /dev/null; then
    echo "[错误] 未检测到 Docker，请先安装 Docker Desktop"
    exit 1
fi
if ! docker info &> /dev/null; then
    echo "[错误] Docker 未运行，请启动 Docker Desktop"
    exit 1
fi
echo "[✓] Docker 状态正常"

# ---- 检查达梦安装包 ----
DM_PKG=$(find "$(dirname "$0")/db/dm8" -name "dm8*.tar.gz" 2>/dev/null | head -1)
if [ -z "$DM_PKG" ]; then
    echo ""
    echo "[重要] 达梦 DM8 安装包未找到！"
    echo ""
    echo "请按以下步骤操作："
    echo "  1. 访问 https://www.dameng.com/document.html 下载 DM8 for Linux x86_64"
    echo "  2. 文件名类似: dm8_2024_xx_xx_x86_install_64.tar.gz"
    echo "  3. 将文件放入: $(dirname "$0")/db/dm8/"
    echo "  4. 重新运行本脚本"
    echo ""
    echo "[提示] 开发阶段可先用 SQLite 运行，漏洞逻辑不受影响"
    echo "       在 config/settings.py 中设置 USE_SQLITE_DEV=True 即可"
    exit 1
fi

echo "[✓] 找到达梦安装包: $DM_PKG"

# ---- 构建达梦镜像 ----
echo "[*] 开始构建达梦 DM8 镜像（首次可能需要几分钟）..."
docker build -f Dockerfile.db -t xinrange/dm8:latest . --no-cache
echo "[✓] 达梦 DM8 镜像构建完成"

# ---- 构建应用镜像 ----
echo "[*] 构建 XinRange 应用镜像..."
docker-compose build

# ---- 启动服务 ----
echo "[*] 启动 XinRange 服务..."
docker-compose up -d

# ---- 等待达梦就绪 ----
echo "[*] 等待达梦数据库就绪（最多等待60秒）..."
for i in $(seq 1 12); do
    if docker exec xinrange-dm8 disql -U SYSDBA -P XinRange2026! -C "SELECT 1 FROM DUAL;" &>/dev/null; then
        echo "[✓] 达梦数据库已就绪"
        break
    fi
    echo "    等待中... ($i/12)"
    sleep 5
done

echo ""
echo "============================================"
echo "  XinRange 启动完成！"
echo "============================================"
echo "  靶场地址: http://localhost:8000"
echo "  管理员:   admin / admin123"
echo "============================================"
