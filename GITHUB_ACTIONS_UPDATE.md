# GitHub Actions Docker 构建配置更新

## 🔧 修复内容

### 问题描述
GitHub Actions 工作流中仍在使用多阶段构建的 `target: app` 和 `target: worker` 参数，但项目已迁移为单服务单容器架构。

### 修复方案

#### 1. 移除多阶段构建目标
**修复前：**
```yaml
- name: Build and push app image to GHCR
  uses: docker/build-push-action@v5
  with:
    target: app  # ❌ 导致错误
    
- name: Build and push worker image to GHCR  
  uses: docker/build-push-action@v5
  with:  
    target: worker  # ❌ 导致错误
```

**修复后：**
```yaml
- name: Build and push Docker image to GHCR
  uses: docker/build-push-action@v5
  with:
    # ✅ 移除 target 参数，使用单阶段构建
    
- name: Build and push Docker image to Docker Hub
  uses: docker/build-push-action@v5
  with:
    # ✅ 移除 target 参数，使用单阶段构建
```

#### 2. 简化构建流程

**之前（多容器）：**
- 构建 `app` 镜像（API + UI）
- 构建 `worker` 镜像（后台任务）
- 需要 4 个构建步骤

**现在（单服务）：**
- 构建单个镜像（包含所有功能）
- 只需要 2 个构建步骤
- 推送到 GHCR 和 Docker Hub

## 🚀 优化效果

### 构建时间优化
- **减少构建步骤**：从 4 个减少到 2 个
- **减少镜像层数**：单阶段构建更高效
- **减少推送时间**：只需推送一个镜像

### 维护成本降低
- **简化 CI/CD 配置**：更少的构建步骤
- **减少镜像管理**：只需维护一个镜像
- **降低存储成本**：减少镜像数量

## 📊 构建配置对比

| 项目 | 多容器架构 | 单服务架构 |
|------|------------|------------|
| 构建步骤 | 4 个 | 2 个 |
| 镜像数量 | 2 个 | 1 个 |
| 构建时间 | 长 | 短 |
| 配置复杂度 | 高 | 低 |
| 维护成本 | 高 | 低 |

## 🎯 验证方法

### 本地验证
```bash
# 验证 Dockerfile 语法
docker build --dry-run -t ai-codereview .

# 实际构建测试
docker build -t ai-codereview .
```

### CI/CD 验证
1. 提交修改到 GitHub
2. 检查 Actions 页面构建状态
3. 验证镜像成功推送到注册表

## ✅ 修复确认

- ✅ 移除了 `target: app` 参数
- ✅ 移除了 `target: worker` 参数  
- ✅ 简化为单服务构建流程
- ✅ 保持了双注册表推送（GHCR + Docker Hub）
- ✅ 保持了多平台构建（linux/amd64, linux/arm64）

---
🎉 **GitHub Actions 工作流已成功更新为单服务架构！**
