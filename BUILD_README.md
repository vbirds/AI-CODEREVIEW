# AI-CodeReview Windows 可执行文件打包指南

本文档说明如何将AI-CodeReview项目打包成Windows可执行文件。

## 🎯 快速开始

### 一键打包
```bash
# 1. 双击运行打包脚本（推荐）
build_windows_exe.bat

# 2. 或者在命令行中运行
./build_windows_exe.bat
```

## 📋 系统要求

### 开发环境要求
- **Windows 10/11** (64位)
- **Python 3.8+** (推荐 Python 3.9-3.11)
- **至少 4GB RAM** (打包过程需要较多内存)
- **5GB 可用磁盘空间** (用于临时文件和输出)

### 目标机器要求
- **Windows 10/11** (64位)
- **无需安装Python** (可执行文件包含所有依赖)
- **2GB RAM** (运行时最低要求)
- **500MB 磁盘空间** (用于数据和日志)

## 🔧 打包流程详解

### 步骤1: 环境准备
```bash
# 安装Python依赖
pip install -r build_requirements.txt

# 或分步安装
pip install pyinstaller>=6.0.0
pip install -r requirements.txt
```

### 步骤2: 配置检查
```bash
# 确保配置文件存在
ls conf/.env

# 如果不存在，复制模板
copy conf_templates\.env.dist conf\.env
```

### 步骤3: 执行打包
```bash
# 使用自定义spec文件打包
pyinstaller --clean ai-codereview.spec

# 或使用基础命令
pyinstaller --onedir --console --name AI-CodeReview launcher.py
```

## 📁 打包输出结构

```
dist/AI-CodeReview/
├── AI-CodeReview.exe          # 主可执行文件
├── 启动AI代码审查.bat          # 快捷启动脚本
├── _internal/                 # PyInstaller内部文件
├── conf/                      # 配置文件目录
├── data/                      # 数据库文件目录
├── log/                       # 日志文件目录
├── biz/                       # 业务逻辑模块
├── ui_components/             # UI组件
├── scripts/                   # 脚本文件
└── 其他必要文件...
```

## 🚀 部署和使用

### 部署到目标机器
1. 将整个 `dist/AI-CodeReview/` 文件夹复制到目标机器
2. 确保目标机器有网络访问权限（用于AI API调用）
3. 配置防火墙允许端口 5001 和 5002

### 启动服务
```bash
# 方法1: 双击启动脚本（推荐）
启动AI代码审查.bat

# 方法2: 直接运行可执行文件
AI-CodeReview.exe

# 方法3: 命令行启动
cd "path\to\AI-CodeReview"
AI-CodeReview.exe
```

### 访问服务
- **API服务**: http://localhost:5001
- **Web界面**: http://localhost:5002
- **默认账号**: admin / admin

## ⚙️ 配置说明

### 首次运行配置
1. 编辑 `conf/.env` 文件
2. 设置AI模型提供商和API密钥:
   ```env
   LLM_PROVIDER=deepseek
   LLM_API_KEY=your_api_key_here
   ```
3. 配置GitLab/GitHub访问令牌
4. 设置消息推送配置（可选）

### 高级配置
- **端口修改**: 在 `.env` 中修改 `API_PORT` 和 `UI_PORT`
- **日志级别**: 设置 `LOG_LEVEL`
- **数据库路径**: 修改 `DB_FILE` 配置

## 🐛 故障排除

### 常见问题

#### 1. 打包失败
```bash
❌ 错误: ModuleNotFoundError
```
**解决方案:**
- 确保所有依赖都已安装: `pip install -r build_requirements.txt`
- 检查Python版本是否兼容 (3.8+)
- 尝试清理缓存: `pip cache purge`

#### 2. 可执行文件启动失败
```bash
❌ 错误: 端口被占用
```
**解决方案:**
- 检查端口5001和5002是否被占用
- 修改配置文件中的端口设置
- 使用 `netstat -an | findstr :5001` 检查端口状态

#### 3. 服务无法访问
```bash
❌ 错误: 无法连接到服务
```
**解决方案:**
- 检查防火墙设置
- 确认服务已正常启动（查看控制台输出）
- 检查配置文件是否正确

#### 4. AI服务调用失败
```bash
❌ 错误: API调用失败
```
**解决方案:**
- 检查API密钥是否正确
- 确认网络连接正常
- 验证AI服务提供商配置

### 调试模式
如需调试，可以修改 `launcher.py` 中的日志级别:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 性能优化

### 减小文件大小
1. **排除不必要的模块**:
   ```python
   # 在 ai-codereview.spec 中添加到 excludes
   excludes=['tkinter', 'matplotlib.backends._tkcairo']
   ```

2. **启用UPX压缩**:
   ```python
   upx=True,
   upx_exclude=[],
   ```

### 提升启动速度
1. **使用 --onefile 模式**（体积更大但启动更快）
2. **预编译字节码**
3. **优化导入顺序**

## 🔒 安全考虑

### 打包安全
- ❌ **不要在打包时包含敏感信息**（API密钥、密码等）
- ✅ **使用环境变量或配置文件**
- ✅ **在生产环境中修改默认密码**

### 运行时安全
- 🔐 **修改默认的Web界面密码**
- 🔑 **使用HTTPS（如果部署到公网）**
- 🛡️ **配置防火墙规则**

## 📞 技术支持

如果遇到问题，请提供以下信息：
1. **操作系统版本**
2. **Python版本**
3. **错误日志** (位于 `log/` 目录)
4. **配置文件内容** (去除敏感信息)

## 🎉 更新说明

### 更新已打包的应用
1. 重新运行打包脚本
2. 备份现有配置文件
3. 用新版本替换可执行文件
4. 恢复配置文件

---

**构建脚本版本**: 1.0.0  
**最后更新**: 2024年  
**兼容版本**: AI-CodeReview v1.0+