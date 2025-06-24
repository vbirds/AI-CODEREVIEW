#!/usr/bin/env python3
"""
AI-CodeReview 代码审查仪表板
重构后的主UI文件 - 模块化设计
"""

import streamlit as st
from ui_components.config import setup_page_config, apply_custom_css
from ui_components.auth import check_authentication, login_page, user_menu
from ui_components.pages import home_page, data_analysis_page, env_management_page
from biz.utils.config_manager import ConfigManager

# 设置页面配置（必须在最开始）
setup_page_config()

# 应用自定义CSS样式
apply_custom_css()

def main_dashboard():
    """主仪表板"""
    
    # 在页面顶部右侧显示用户菜单
    user_menu()
    
    # 侧边栏 - 简化布局
    with st.sidebar:
        # 功能菜单
        st.markdown("### 🛠️ 系统功能")
        
        # 页面导航 - 使用更直观的布局
        page = st.radio(
            "选择功能模块",
            ["🏠 首页", "📊 数据分析", "⚙️ 配置管理"],
            key="page_selector",
            help="选择要访问的功能模块"
        )
        
        st.markdown("---")
        
        # 系统信息
        st.markdown("### ℹ️ 系统信息")
        
        # 获取系统状态
        try:
            config_manager = ConfigManager()
            env_config = config_manager.get_env_config()
            configured_count = len([v for v in env_config.values() if v and v.strip()])
            total_count = len(env_config)
            
            st.metric("配置完成度", f"{configured_count}/{total_count}")
            st.metric("当前AI模型", env_config.get("LLM_PROVIDER", "未配置"))
        except:
            st.info("配置信息加载中...")
        
        # 帮助信息
        st.markdown("---")
        with st.expander("📖 使用帮助"):
            st.markdown("""
            **🏠 首页**: 系统概览和快速开始指南
            
            **📊 数据分析**: 查看代码审查统计和详细记录
            
            **⚙️ 配置管理**: 管理AI模型、平台开关等系统配置
            
            **用户操作**: 
            - 👤 点击右上角用户名可注销登录
            """)
    
    # 根据选择的页面显示内容
    if page == "⚙️ 配置管理":
        env_management_page()
    elif page == "📊 数据分析":
        data_analysis_page()
    else:  # 首页
        home_page()

def main():
    """主函数"""
    # 检查认证状态
    if not check_authentication():
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
