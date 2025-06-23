# 🚀 自动化构建和发布已配置完成

## ✅ 已实现的自动化功能

### 1. 自动Docker镜像构建和发布

当你提交代码到GitHub后，系统会自动：

- **代码推送触发**: 推送到`main`、`master`、`develop`分支时自动构建
- **标签发布触发**: 创建`v*.*.*`格式的标签时自动构建和发布
- **多平台支持**: 自动构建`linux/amd64`和`linux/arm64`两个平台的镜像
- **多镜像类型**: 自动构建`app`(应用)和`worker`(工作进程)两种镜像

### 2. 发布到GitHub Container Registry

镜像会自动发布到：
- `ghcr.io/zhao-zg/ai-codereview-gitlab:latest` (最新版本)
- `ghcr.io/zhao-zg/ai-codereview-gitlab:latest-worker` (工作进程)
- `ghcr.io/zhao-zg/ai-codereview-gitlab:v1.2.3` (特定版本)
- `ghcr.io/zhao-zg/ai-codereview-gitlab:v1.2.3-worker` (特定版本工作进程)

## 📋 配置文件说明

已创建和配置的文件：

```
.github/workflows/
├── docker-build.yml      # 主要的Docker构建和发布工作流
├── test-docker.yml       # Docker构建测试工作流
├── test.yml              # 代码测试工作流
├── release.yml           # 版本发布工作流
└── update-deps.yml       # 依赖更新工作流

scripts/
├── test_docker_local.py  # 本地Docker构建测试脚本
├── release.py            # 版本发布管理脚本
└── check_ci_status.py    # CI状态检查脚本

docs/
└── auto-build-guide.md   # 详细使用指南
```

## 🎯 如何使用

### 方法1: 直接推送代码（推荐）

```bash
# 开发完成后推送代码
git add .
git commit -m "feat: 添加新功能"
git push origin main      # 自动触发构建

# 系统会自动：
# 1. 运行测试
# 2. 构建Docker镜像
# 3. 发布到ghcr.io
# 4. 更新latest标签
```

### 方法2: 创建版本标签

```bash
# 使用发布脚本（推荐）
python scripts/release.py --increment patch

# 或手动创建标签
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3

# 系统会自动：
# 1. 构建带版本号的镜像
# 2. 创建GitHub Release
# 3. 生成更新日志
```

### 方法3: 手动触发构建

在GitHub仓库页面：
1. 进入"Actions"标签页
2. 选择"Build and Publish Docker Images"工作流
3. 点击"Run workflow"按钮

## 🔍 监控构建状态

### 查看GitHub Actions

访问：https://github.com/zhao-zg/AI-CODEREVIEW-GITLAB/actions

### 使用命令行检查

```bash
# 检查CI状态和镜像发布情况
python scripts/check_ci_status.py

# 只检查CI状态
python scripts/check_ci_status.py --check-ci

# 只检查镜像状态  
python scripts/check_ci_status.py --check-image
```

## 🐳 使用发布的镜像

### 拉取镜像

```bash
# 拉取最新版本
docker pull ghcr.io/zhao-zg/ai-codereview-gitlab:latest
docker pull ghcr.io/zhao-zg/ai-codereview-gitlab:latest-worker

# 拉取特定版本
docker pull ghcr.io/zhao-zg/ai-codereview-gitlab:v1.2.3
docker pull ghcr.io/zhao-zg/ai-codereview-gitlab:v1.2.3-worker
```

### 使用docker-compose

```bash
# 使用已更新的docker-compose.yml
docker-compose up -d

# 系统会自动使用最新的镜像
```

## 📝 工作流详情

### Docker构建工作流特性

- ✅ **多阶段构建**: 支持`app`和`worker`两种镜像类型
- ✅ **多平台构建**: 支持AMD64和ARM64架构
- ✅ **缓存优化**: 使用GitHub Actions缓存加速构建
- ✅ **自动标签**: 根据分支和标签自动生成镜像标签
- ✅ **权限管理**: 自动处理GitHub Container Registry认证

### 触发条件

| 事件 | 分支/标签 | 生成的镜像标签 |
|------|-----------|---------------|
| Push | main/master | `latest`, `latest-worker` |
| Push | develop | `develop`, `develop-worker` |
| Tag | v1.2.3 | `v1.2.3`, `v1.2.3-worker`, `1.2.3`, `1.2`, `1`, `latest` |

## 🔧 故障排除

### 构建失败

1. 检查GitHub Actions日志
2. 验证Dockerfile语法
3. 确认requirements.txt中的依赖

### 镜像拉取失败

1. 确认镜像名称正确
2. 检查网络连接
3. 验证GitHub Container Registry访问权限

## 🔧 环境配置自动化

### .env文件自动创建

系统提供多种方式自动创建和管理环境配置：

#### 方法1: 使用快速启动脚本（推荐）

```bash
# 自动检查并创建.env文件，然后启动服务
python quick_start.py
```

脚本会自动：
- 创建必要目录
- 检查.env文件是否存在
- 从.env.dist模板创建.env（如果存在）
- 或创建包含所有配置项的默认.env文件
- 检查API密钥配置并给出提示
- 启动Docker服务

#### 方法2: 使用一键启动脚本

```bash
# Windows
start_docker.bat

# Linux/Mac
./start_docker.sh
```

#### 方法3: 容器内自动创建

如果启动容器时没有.env文件，容器会自动：
- 运行初始化脚本
- 创建默认配置文件
- 加载环境变量

### 配置检查和提醒

所有启动方式都会：
- ✅ 检查API密钥是否配置
- ⚠️ 给出配置提醒和指导
- 💡 提供配置建议（推荐DeepSeek）

## 🎉 总结

自动化构建和发布功能已完全配置完成！你现在可以：

1. **无忧推送**: 直接推送代码，系统自动构建和发布
2. **版本管理**: 使用脚本轻松管理版本发布
3. **监控状态**: 随时检查构建和镜像状态
4. **多平台支持**: 自动构建支持多种CPU架构的镜像

只需要正常提交代码，GitHub Actions会自动处理所有的构建和发布工作！🚀

---

📖 **详细使用指南**: 请查看 [docs/auto-build-guide.md](docs/auto-build-guide.md)
