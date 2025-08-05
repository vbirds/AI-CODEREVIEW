# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path(os.path.abspath('.'))

# 分析主要的Python文件
a = Analysis(
    ['launcher.py'],  # 启动器脚本
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # 配置文件和模板
        ('conf', 'conf'),
        ('conf_templates', 'conf_templates'),
        
        # UI组件
        ('ui_components', 'ui_components'),
        
        # 业务逻辑模块
        ('biz', 'biz'),
        
        # 脚本文件
        ('scripts', 'scripts'),
        
        # 文档
        ('docs', 'docs'),
        
        # 数据目录（如果存在）
        ('data', 'data') if os.path.exists('data') else ('', ''),
        
        # 日志目录（如果存在）
        ('log', 'log') if os.path.exists('log') else ('', ''),
        
        # requirements.txt
        ('requirements.txt', '.'),
        
        # README和其他文档
        ('README.md', '.'),
        ('CLAUDE.md', '.'),
        ('CHANGELOG.md', '.'),
        
        # Docker配置（用于参考）
        ('docker-compose.yml', '.'),
        ('Dockerfile', '.'),
        
    ],
    hiddenimports=[
        # Flask相关
        'flask',
        'flask.json',
        'flask.logging',
        
        # Streamlit相关
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        
        # 数据处理
        'pandas',
        'numpy',
        'matplotlib',
        'plotly',
        
        # HTTP和网络
        'requests',
        'httpx',
        'urllib3',
        
        # 配置和环境
        'python_dotenv',
        'yaml',
        'configparser',
        
        # 调度器
        'apscheduler',
        'apscheduler.schedulers.background',
        'apscheduler.triggers.cron',
        
        # 数据库
        'sqlite3',
        'pymysql',
        
        # AI相关
        'openai',
        'zhipuai',
        'ollama',
        'tiktoken',
        
        # 其他工具库
        'schedule',
        'watchdog',
        'psutil',
        'portalocker',
        'lizard',
        'pathspec',
        'tabulate',
        'rq',
        'pytz',
        
        # 项目内部模块
        'biz',
        'biz.service',
        'biz.service.review_service',
        'biz.llm',
        'biz.llm.factory',
        'biz.queue',
        'biz.queue.worker',
        'biz.utils',
        'biz.utils.log',
        'biz.utils.config_manager',
        'biz.gitlab',
        'biz.github',
        'biz.svn',
        'ui_components',
        'ui_components.auth',
        'ui_components.pages',
        'ui_components.config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除一些不需要的模块
        'tkinter',
        'test',
        'unittest',
        'pydoc',
        'doctest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI-CodeReview',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 保持控制台窗口以便查看日志
    icon=None,  # 可以添加图标文件
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI-CodeReview',
)