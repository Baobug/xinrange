# XinRange - 信创渗透靶场
> 基于银河麒麟 V10 + 达梦 DM8 的渗透学习平台，涵盖 OWASP Top 10 漏洞场景

## 技术栈

| 层次 | 技术选型 |
|------|----------|
| 操作系统（目标） | 银河麒麟 V10 SP2 (x86_64) |
| 数据库 | 达梦 DM8 |
| 后端框架 | Python Django 4.x |
| 前端 | Vue 3 + Vite |
| 容器化 | Docker + Docker Compose |

## 项目结构

```
XinRange/
├── docker-compose.yml      # 容器编排（DM8 + App + Nginx）
├── Dockerfile.app          # 应用服务镜像
├── Dockerfile.db           # 达梦数据库镜像（可选自定义）
├── app/
│   ├── core/               # 核心模块：用户、积分、难度管理
│   ├── vulns/              # 漏洞模块目录
│   │   ├── sqli/          # SQL 注入（达梦方言）
│   │   ├── xss/            # XSS 跨站脚本
│   │   ├── upload/         # 文件上传
│   │   ├── cmd_injection/  # 命令注入
│   │   └── ...
│   ├── templates/          # Django 模板
│   └── static/             # 静态资源
├── db/
│   └── init/               # 达梦初始化 SQL 脚本
├── docs/                   # 设计文档
└── README.md
```

## 快速启动

### 前置条件
- Docker 20.10+
- Docker Compose v2+

### 启动步骤

```bash
# 1. 克隆项目
git clone https://github.com/yourname/xinrange.git
cd xinrange

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，修改达梦连接密码等配置

# 3. 一键启动
docker-compose up -d

# 4. 访问靶场
open http://localhost:8000
```

默认管理员账号：`admin` / `admin123`

## 漏洞模块计划

### Phase 1（MVP）
- [ ] SQL 注入 — 达梦 DM8 方言（UNION、布尔、报错注入）
- [ ] XSS 存储型/反射型
- [ ] 文件上传绕过
- [ ] 命令注入

### Phase 2
- [ ] 身份认证缺陷（暴力破解、Session 固定）
- [ ] 敏感信息泄露
- [ ] XML 外部实体（XXE）
- [ ] 访问控制失效（越权）

### Phase 3
- [ ] 不安全反序列化
- [ ] CSRF
- [ ] SSRF
- [ ] 国产中间件专项（东方通TongWeb、宝兰德）

## 难度分级

每个漏洞模块均包含三级难度：

| 等级 | 说明 |
|------|------|
| 🔵 Low | 代码直接暴露漏洞，无任何过滤，参考 DVWA Low |
| 🟡 Medium | 存在基础过滤或简单绕过，适合入门 |
| 🔴 High | 接近真实环境，需要组合利用技巧 |

## 免责声明

XinRange 仅供合法网络安全学习与研究使用。
禁止利用本项目对任何未授权系统进行渗透测试。
违反使用规定者，自行承担法律责任。
