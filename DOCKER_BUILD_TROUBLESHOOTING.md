# Docker 构建故障排除指南

## 问题：ERROR: failed to solve: target stage "app" could not be found

### 🔍 问题分析

这个错误通常发生在以下情况：

1. **使用了错误的构建命令**：尝试使用多阶段构建的 `--target` 参数
2. **Docker 缓存问题**：缓存了之前的多阶段构建信息
3. **使用了过时的文档或脚本**

### ✅ 解决方案

#### 1. 使用正确的构建命令

**正确的单服务构建命令：**
```bash
# 基本构建
docker build -t ai-codereview .

# 清除缓存重新构建
docker build --no-cache -t ai-codereview .

# 使用 docker-compose 构建
docker-compose build

# 强制重新构建
docker-compose build --no-cache
```

**❌ 错误的命令（不要使用）：**
```bash
# 这些命令会导致错误，因为当前是单阶段构建
docker build --target app -t ai-codereview .
docker build --target worker -t ai-codereview .
```

#### 2. 清理 Docker 缓存

```bash
# 清理构建缓存
docker builder prune

# 清理所有未使用的镜像
docker image prune -a

# 完全清理（谨慎使用）
docker system prune -a
```

#### 3. 验证 Dockerfile

当前的 Dockerfile 是单阶段构建，正确的结构：

```dockerfile
# 单阶段构建 - 所有功能在一个阶段完成
FROM python:3.12-slim
WORKDIR /app
# ... 安装和配置 ...
CMD ["/app/start.sh"]
```

### 🚀 推荐的构建流程

#### 本地开发
```bash
# 1. 构建镜像
docker build -t ai-codereview .

# 2. 运行容器
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

#### 生产部署
```bash
# 1. 拉取最新代码
git pull

# 2. 构建并启动
docker-compose up -d --build

# 3. 验证服务
curl http://localhost:5001
curl http://localhost:5002
```

### 🔧 架构说明

**当前架构（单服务）：**
- ✅ 一个容器包含所有功能
- ✅ API + UI + Worker 在同一进程中
- ✅ 使用内存队列，无需 Redis
- ✅ 简化部署和运维

**之前架构（多容器）：**
- ❌ 需要多个容器协调
- ❌ 需要 Redis 等外部依赖
- ❌ 部署复杂，运维困难

### 📝 常见问题

1. **网络连接问题**
   ```bash
   # 如果无法下载基础镜像，检查网络连接
   docker pull python:3.12-slim
   ```

2. **权限问题**
   ```bash
   # 确保 Docker 服务正在运行
   docker version
   ```

3. **端口冲突**
   ```bash
   # 检查端口是否被占用
   netstat -tlnp | grep 5001
   netstat -tlnp | grep 5002
   ```

### 🎯 成功构建验证

构建成功后，您应该看到：
```bash
# 检查镜像
docker images | grep ai-codereview

# 检查运行状态
docker-compose ps

# 测试服务
curl http://localhost:5001/health
```

---
✅ **总结**：使用单阶段构建命令，清理缓存，避免使用 `--target` 参数。
