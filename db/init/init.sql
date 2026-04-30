-- ============================================================
-- XinRange 达梦 DM8 数据库初始化脚本
-- 靶场漏洞场景数据
-- ============================================================

-- 创建 sqli_users 表（SQL 注入演示用户）
CREATE TABLE IF NOT EXISTS sqli_users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(128),
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user'
);

INSERT INTO sqli_users (username, password, email, role) VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@xinrange.local', 'admin'),
('guest', '084e0343a0486ff05530df6c705c8bb4', 'guest@xinrange.local', 'user'),
('tester', '098f6bcd4621d373cade4e832627b4f6', 'test@xinrange.local', 'user');

-- 创建 sqli_posts 表（SQL 注入演示文章）
CREATE TABLE IF NOT EXISTS sqli_posts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    author VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sqli_posts (title, content, author) VALUES
('欢迎来到XinRange', '这是一个基于信创平台的渗透学习靶场...', 'admin'),
('达梦数据库SQL注入技巧', '本文介绍达梦DM8特有的SQL注入方式...', 'admin'),
('XSS漏洞利用详解', '跨站脚本攻击是最常见的Web漏洞之一...', 'admin'),
('文件上传绕过技术', '探讨各种文件上传绕过方法...', 'guest');

-- 创建 xss_comments 表（XSS 演示评论）
CREATE TABLE IF NOT EXISTS xss_comments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50),
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO xss_comments (username, content) VALUES
('system', '欢迎留言讨论！'),
('guest', '这个靶场很不错');

-- 创建 upload_files 表（文件上传记录）
CREATE TABLE IF NOT EXISTS upload_files (
    id INT IDENTITY(1,1) PRIMARY KEY,
    filename VARCHAR(255),
    filepath VARCHAR(500),
    uploader VARCHAR(50),
    size INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建 cmd_results 表（命令注入 Ping 结果）
CREATE TABLE IF NOT EXISTS cmd_results (
    id INT IDENTITY(1,1) PRIMARY KEY,
    target VARCHAR(200),
    result TEXT,
    executed_by VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

COMMIT;
