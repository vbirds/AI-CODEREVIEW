@echo off
chcp 65001
echo ========================================
echo AI-CodeReview Windows 可执行文件打包工具
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

:: 检查Python环境
echo [1/8] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)
python --version

:: 检查pip
echo.
echo [2/8] 检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到pip，请检查Python安装
    pause
    exit /b 1
)

:: 安装PyInstaller（如果未安装）
echo.
echo [3/8] 检查PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📦 安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ 错误: PyInstaller安装失败
        pause
        exit /b 1
    )
) else (
    echo ✅ PyInstaller已安装
)

:: 安装项目依赖
echo.
echo [4/8] 安装项目依赖...
if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ⚠️ 警告: 部分依赖安装失败，继续打包...
    ) else (
        echo ✅ 依赖安装完成
    )
) else (
    echo ⚠️ 警告: 未找到requirements.txt文件
)

:: 创建必要目录
echo.
echo [5/8] 创建必要目录...
if not exist "data" mkdir data
if not exist "log" mkdir log
if not exist "conf" mkdir conf

:: 检查配置文件
echo.
echo [6/8] 检查配置文件...
if not exist "conf\.env" (
    if exist "conf_templates\.env.dist" (
        echo 📋 复制默认配置文件...
        copy "conf_templates\.env.dist" "conf\.env"
    ) else (
        echo ⚠️ 警告: 未找到配置模板文件
    )
)

:: 清理之前的构建
echo.
echo [7/8] 清理之前的构建...
if exist "dist" (
    echo 🧹 清理dist目录...
    rmdir /s /q "dist"
)
if exist "build" (
    echo 🧹 清理build目录...
    rmdir /s /q "build"
)

:: 开始打包
echo.
echo [8/8] 开始打包...
echo 📦 使用PyInstaller打包，这可能需要几分钟时间...
echo.

pyinstaller --clean ai-codereview.spec

if errorlevel 1 (
    echo.
    echo ❌ 打包失败！请检查错误信息。
    echo.
    echo 常见问题解决方案:
    echo 1. 检查Python版本是否为3.8+
    echo 2. 确保所有依赖都已正确安装
    echo 3. 检查是否有杀毒软件干扰
    echo 4. 尝试以管理员身份运行此脚本
    echo.
    pause
    exit /b 1
)

:: 检查打包结果
echo.
if exist "dist\AI-CodeReview" (
    echo ✅ 打包成功！
    echo.
    echo 📁 可执行文件位置: dist\AI-CodeReview\
    echo 🚀 启动文件: dist\AI-CodeReview\AI-CodeReview.exe
    echo.
    
    :: 创建快捷启动脚本
    echo @echo off > "dist\AI-CodeReview\启动AI代码审查.bat"
    echo chcp 65001 >> "dist\AI-CodeReview\启动AI代码审查.bat"
    echo echo 启动AI代码审查服务... >> "dist\AI-CodeReview\启动AI代码审查.bat"
    echo AI-CodeReview.exe >> "dist\AI-CodeReview\启动AI代码审查.bat"
    echo pause >> "dist\AI-CodeReview\启动AI代码审查.bat"
    
    echo 📋 使用说明:
    echo 1. 将 dist\AI-CodeReview 文件夹复制到目标机器
    echo 2. 双击 "启动AI代码审查.bat" 或直接运行 AI-CodeReview.exe
    echo 3. API服务将在 http://localhost:5001 启动
    echo 4. Web界面将在 http://localhost:5002 启动
    echo.
    
    :: 计算文件夹大小
    echo 📊 打包信息:
    for /f %%A in ('dir "dist\AI-CodeReview" /s /-c ^| find "个文件"') do echo 文件数量: %%A
    
    echo.
    echo 🎉 打包完成！是否现在打开输出目录？(Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        explorer "dist\AI-CodeReview"
    )
    
) else (
    echo ❌ 打包失败: 未找到输出文件
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成
echo ========================================
pause