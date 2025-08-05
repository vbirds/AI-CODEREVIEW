#!/usr/bin/env python3
"""
AI-CodeReview Windows可执行文件启动器
统一启动API服务和Web UI界面的主入口点
"""

import os
import sys
import threading
import time
import signal
import subprocess
import webbrowser
from pathlib import Path
import multiprocessing
import logging

# 设置编码
if sys.platform == 'win32':
    import locale
    locale.setlocale(locale.LC_ALL, 'Chinese (Simplified)_China.936')

# 获取可执行文件所在目录
if getattr(sys, 'frozen', False):
    # PyInstaller打包后的路径
    APP_DIR = Path(sys.executable).parent
else:
    # 开发环境路径
    APP_DIR = Path(__file__).parent

# 设置工作目录
os.chdir(APP_DIR)

# 添加项目路径到sys.path
sys.path.insert(0, str(APP_DIR))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log/launcher.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('launcher')

class ServiceManager:
    """服务管理器"""
    
    def __init__(self):
        self.api_process = None
        self.ui_process = None
        self.running = True
        
    def check_and_create_dirs(self):
        """检查并创建必要的目录"""
        dirs = ['conf', 'data', 'log']
        for dir_name in dirs:
            dir_path = APP_DIR / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"创建目录: {dir_path}")
    
    def check_config(self):
        """检查配置文件"""
        env_file = APP_DIR / 'conf' / '.env'
        env_template = APP_DIR / 'conf_templates' / '.env.dist'
        
        if not env_file.exists():
            if env_template.exists():
                import shutil
                shutil.copy2(env_template, env_file)
                logger.info(f"复制配置模板: {env_template} -> {env_file}")
            else:
                # 创建基本配置文件
                basic_config = """# AI-CodeReview 基础配置
LLM_PROVIDER=deepseek
LLM_API_KEY=your_api_key_here
API_PORT=5001
UI_PORT=5002
LOG_LEVEL=INFO
ENABLE_API=true
ENABLE_UI=true
"""
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(basic_config)
                logger.info(f"创建基础配置文件: {env_file}")
    
    def init_database(self):
        """初始化数据库"""
        try:
            from biz.service.review_service import ReviewService
            ReviewService.init_db()
            logger.info("数据库初始化完成")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
    
    def start_api_service(self):
        """启动API服务"""
        def run_api():
            try:
                logger.info("启动API服务 (端口: 5001)")
                
                # 加载环境配置
                from dotenv import load_dotenv
                load_dotenv("conf/.env")
                
                # 导入并启动API应用
                from api import api_app
                api_app.run(
                    host='0.0.0.0',
                    port=int(os.getenv('API_PORT', '5001')),
                    debug=False,
                    use_reloader=False,
                    threaded=True
                )
            except Exception as e:
                logger.error(f"API服务启动失败: {e}")
                
        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        return api_thread
    
    def start_ui_service(self):
        """启动UI服务"""
        def run_ui():
            try:
                logger.info("启动Web UI服务 (端口: 5002)")
                
                # 设置Streamlit配置
                os.environ['STREAMLIT_SERVER_PORT'] = os.getenv('UI_PORT', '5002')
                os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
                os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
                os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
                
                # 导入并启动UI
                import streamlit.web.cli as stcli
                import streamlit as st
                
                # 修改sys.argv来模拟命令行参数
                sys.argv = [
                    "streamlit",
                    "run",
                    str(APP_DIR / "ui.py"),
                    "--server.port", os.getenv('UI_PORT', '5002'),
                    "--server.address", "0.0.0.0",
                    "--server.headless", "true",
                    "--browser.gatherUsageStats", "false"
                ]
                
                stcli.main()
                
            except Exception as e:
                logger.error(f"UI服务启动失败: {e}")
                
        ui_thread = threading.Thread(target=run_ui, daemon=True)
        ui_thread.start()
        return ui_thread
    
    def wait_for_services(self):
        """等待服务启动"""
        import requests
        import time
        
        # 等待API服务
        api_port = os.getenv('API_PORT', '5001')
        ui_port = os.getenv('UI_PORT', '5002')
        
        logger.info("等待服务启动...")
        
        for i in range(30):  # 最多等待30秒
            try:
                # 检查API服务
                response = requests.get(f'http://localhost:{api_port}', timeout=2)
                if response.status_code == 200:
                    logger.info(f"✅ API服务已启动: http://localhost:{api_port}")
                    break
            except:
                time.sleep(1)
        
        time.sleep(3)  # 额外等待UI服务启动
        logger.info(f"✅ Web界面地址: http://localhost:{ui_port}")
    
    def open_browser(self):
        """打开浏览器"""
        try:
            ui_port = os.getenv('UI_PORT', '5002')
            url = f'http://localhost:{ui_port}'
            
            time.sleep(5)  # 等待服务完全启动
            webbrowser.open(url)
            logger.info(f"已打开浏览器: {url}")
        except Exception as e:
            logger.error(f"打开浏览器失败: {e}")
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        logger.info(f"收到信号 {signum}，正在关闭服务...")
        self.running = False
        sys.exit(0)
    
    def setup_signal_handlers(self):
        """设置信号处理器"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Windows特定
        if sys.platform == 'win32':
            signal.signal(signal.SIGBREAK, self.signal_handler)
    
    def run(self):
        """主运行函数"""
        print("=" * 50)
        print("🚀 AI-CodeReview 代码审查系统")
        print("=" * 50)
        
        # 设置信号处理
        self.setup_signal_handlers()
        
        # 初始化
        logger.info("初始化系统...")
        self.check_and_create_dirs()
        self.check_config()
        self.init_database()
        
        # 启动服务
        logger.info("启动服务...")
        api_thread = self.start_api_service()
        ui_thread = self.start_ui_service()
        
        # 等待服务启动
        self.wait_for_services()
        
        # 打开浏览器
        browser_thread = threading.Thread(target=self.open_browser, daemon=True)
        browser_thread.start()
        
        # 显示启动信息
        api_port = os.getenv('API_PORT', '5001')
        ui_port = os.getenv('UI_PORT', '5002')
        
        print("\n🎉 服务启动成功！")
        print(f"📡 API服务地址: http://localhost:{api_port}")
        print(f"🌐 Web界面地址: http://localhost:{ui_port}")
        print("\n默认登录账号: admin / admin")
        print("\n按 Ctrl+C 停止服务")
        print("=" * 50)
        
        # 保持主线程运行
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("用户中断，正在关闭服务...")
        finally:
            logger.info("服务已关闭")

def main():
    """主函数"""
    try:
        # 设置多进程启动方法（Windows兼容）
        if sys.platform == 'win32':
            multiprocessing.set_start_method('spawn', force=True)
        
        manager = ServiceManager()
        manager.run()
        
    except Exception as e:
        logger.error(f"启动失败: {e}")
        print(f"\n❌ 启动失败: {e}")
        print("\n请检查:")
        print("1. 是否有其他程序占用端口 5001 或 5002")
        print("2. 配置文件是否正确")
        print("3. 是否有权限问题")
        input("\n按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()