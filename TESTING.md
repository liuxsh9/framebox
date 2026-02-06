# framebox 测试指南

## 环境准备

### 1. 安装 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 创建虚拟环境并安装依赖

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境 (可选，uv 会自动使用)
source .venv/bin/activate

# 安装项目依赖
uv pip install -e .
```

### 3. 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置 (如果需要修改端口等)
nano .env
```

## 启动服务器

### 方式 1: 直接运行（开发模式）

```bash
# 使用 uv 运行（推荐）
uv run python main.py

# 或者使用 uvicorn
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

服务器将在 `http://localhost:8001` 启动（默认端口可在 .env 中修改）

### 方式 2: 使用 pm2（生产模式）

```bash
# 安装 pm2 (如果还没有)
npm install -g pm2

# 启动服务
pm2 start ecosystem.config.js

# 查看状态
pm2 list

# 查看日志
pm2 logs framebox

# 停止服务
pm2 stop framebox
```

## 自动化测试

### 运行测试脚本

```bash
# 确保服务器正在运行
uv run python main.py &

# 等待服务器启动
sleep 3

# 运行测试
./test.sh

# 测试完成后停止服务器
pkill -f "uv run python main.py"
```

### 测试覆盖范围

测试脚本 (`test.sh`) 包含以下测试：

1. ✓ Health check endpoint
2. ✓ Project creation
3. ✓ Duplicate name rejection (409)
4. ✓ List projects
5. ✓ Get project by ID
6. ✓ Get project by name
7. ✓ File upload (batch with nested path)
8. ✓ List project files
9. ✓ Serve entry file by ID
10. ✓ Serve entry file by name
11. ✓ Serve nested file
12. ✓ Serve JSON file
13. ✓ CORS headers present
14. ✓ Path validation (reject ..)
15. ✓ Project update
16. ✓ Search functionality
17. ✓ Project deletion
18. ✓ Verify deletion (404)

## 手动测试

### 1. 测试健康检查

```bash
curl http://localhost:8001/api/health
# 预期: {"status":"ok","uptime":123.45}
```

### 2. 创建项目

```bash
curl -X POST http://localhost:8001/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "my-test-project", "entry_file": "index.html"}'

# 预期返回项目信息，记下 id (例如: "k3x9p2")
```

### 3. 上传文件

创建测试文件：

```bash
mkdir -p /tmp/test-project
cat > /tmp/test-project/index.html <<'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Test Project</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Hello from framebox!</h1>
    <div id="data"></div>
    <script>
        fetch('./data.json')
            .then(r => r.json())
            .then(data => {
                document.getElementById('data').textContent = data.message;
            });
    </script>
</body>
</html>
EOF

cat > /tmp/test-project/style.css <<'EOF'
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    background: #f0f0f0;
}
h1 { color: #333; }
EOF

cat > /tmp/test-project/data.json <<'EOF'
{
    "message": "Data loaded successfully from framebox!"
}
EOF
```

上传文件（替换 PROJECT_ID 为你的项目ID）：

```bash
PROJECT_ID="k3x9p2"  # 替换为实际的项目 ID

curl -X POST http://localhost:8001/api/projects/$PROJECT_ID/files \
  -F "files=@/tmp/test-project/index.html" \
  -F "files=@/tmp/test-project/style.css" \
  -F "files=@/tmp/test-project/data.json"
```

### 4. 访问项目

在浏览器中打开：

- 通过 ID: `http://localhost:8001/view/k3x9p2/`
- 通过名称: `http://localhost:8001/view/my-test-project/`

你应该看到渲染后的 HTML 页面，包含样式和动态加载的数据。

### 5. 测试 Web UI

在浏览器中打开 `http://localhost:8001/`

功能测试：
- ✓ 查看项目列表
- ✓ 搜索项目
- ✓ 创建新项目
- ✓ 上传文件（拖拽或点击上传）
- ✓ 预览项目
- ✓ 复制嵌入代码
- ✓ 删除项目

### 6. 测试 Markdown 嵌入

创建一个 Markdown 文件：

```markdown
# 我的文档

这是一个嵌入的图表:

<iframe src="http://localhost:8001/view/k3x9p2/" width="800" height="600" frameborder="0"></iframe>

或者使用名称:

<iframe src="http://localhost:8001/view/my-test-project/" width="800" height="600" frameborder="0"></iframe>
```

使用 Markdown 预览工具查看效果。

### 7. 测试 API 文档

FastAPI 自动生成的 API 文档：

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

可以在这里交互式测试所有 API 端点。

## pm2 部署测试

### 1. 启动服务

```bash
pm2 start ecosystem.config.js
pm2 save
```

### 2. 测试自动重启

```bash
# 杀死进程测试自动重启
pm2 delete framebox
pm2 start ecosystem.config.js

# 查看日志确认重启
pm2 logs framebox --lines 50
```

### 3. 测试开机自启

```bash
# 配置开机自启
pm2 startup

# 保存当前进程列表
pm2 save

# 重启系统后检查
pm2 list
```

### 4. 测试内存限制

```bash
# ecosystem.config.js 配置了 max_memory_restart: '500M'
# 监控内存使用
pm2 monit
```

## 局域网访问测试

### 1. 确认服务器绑定到 0.0.0.0

```bash
netstat -an | grep 8001
# 应该看到: *.8001 或 0.0.0.0:8001
```

### 2. 获取本机 IP

```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# 或者
hostname -I
```

### 3. 从其他设备访问

在同一局域网的其他设备上:

```
http://192.168.x.x:8001/
```

替换 `192.168.x.x` 为你的实际 IP 地址。

## 性能测试

### 并发请求测试

```bash
# 安装 apache bench (如果需要)
# macOS: brew install apache-bench
# Linux: apt-get install apache2-utils

# 测试健康检查端点
ab -n 1000 -c 10 http://localhost:8001/api/health

# 测试静态文件服务
ab -n 1000 -c 10 http://localhost:8001/view/k3x9p2/
```

### 大文件上传测试

```bash
# 创建一个接近 50MB 的文件（当前限制）
dd if=/dev/zero of=/tmp/large.html bs=1M count=45

# 上传测试
curl -X POST http://localhost:8001/api/projects/$PROJECT_ID/files \
  -F "files=@/tmp/large.html" \
  -w "Time: %{time_total}s\n"
```

## 常见问题排查

### 端口被占用

```bash
# 查看占用端口的进程
lsof -i :8001

# 修改端口
echo "PORT=8002" >> .env
```

### 数据库锁定

```bash
# 确保只有一个服务器实例在运行
ps aux | grep "python main.py"
pkill -f "python main.py"

# 重新启动
python main.py
```

### 文件权限问题

```bash
# 确保数据目录可写
chmod -R 755 data/
```

### CORS 问题

```bash
# 检查响应头
curl -v http://localhost:8001/view/k3x9p2/ 2>&1 | grep -i "access-control"

# 应该看到:
# access-control-allow-origin: *
# access-control-allow-methods: *
# access-control-allow-headers: *
```

## 清理测试数据

```bash
# 停止服务器
pm2 stop framebox
# 或
pkill -f "uv run python"

# 删除所有测试数据
rm -rf data/

# 重新创建目录
mkdir -p data/projects

# 重启服务器
uv run python main.py
```

## 下一步

- 部署到生产服务器
- 配置反向代理 (Nginx/Caddy)
- 设置 HTTPS
- 配置备份策略
- 监控和日志聚合
