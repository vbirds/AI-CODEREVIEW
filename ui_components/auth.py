"""
认证相关功能模块 - 基于配置文件的认证
"""

import os
import json
import hashlib
import tempfile
import pandas as pd
import streamlit as st
from biz.utils.config_manager import ConfigManager

def authenticate(username, password):
    """基于配置文件的用户认证"""
    try:
        config_manager = ConfigManager()
        env_config = config_manager.get_env_config()
        
        # 从环境配置中获取Dashboard账户信息
        dashboard_username = env_config.get('DASHBOARD_USER', 'admin')
        dashboard_password = env_config.get('DASHBOARD_PASSWORD', 'admin')
        
        return username == dashboard_username and password == dashboard_password
    except Exception as e:
        st.error(f"认证配置读取失败: {e}")
        # 使用默认认证作为fallback
        return username == "admin" and password == "admin"

def get_session_file_path():
    """
    获取当前会话的持久化文件路径
    基于Streamlit的session ID创建唯一标识
    """
    try:
        # 获取Streamlit的session_id
        from streamlit.runtime import get_instance
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        
        runtime = get_instance()
        if runtime and runtime.is_ready:
            session_id = get_script_run_ctx().session_id if get_script_run_ctx() else None
            if session_id:
                # 使用session_id的hash作为文件名
                session_hash = hashlib.md5(session_id.encode()).hexdigest()[:16]
                return os.path.join(tempfile.gettempdir(), f"ai_codereview_session_{session_hash}.json")
    except:
        pass
    
    # 如果无法获取session_id，使用fallback方案
    fallback_id = str(hash(str(st.session_state)))[:16].replace('-', '0')
    return os.path.join(tempfile.gettempdir(), f"ai_codereview_session_{fallback_id}.json")

def save_login_state(username):
    """保存登录状态到持久化文件"""
    try:
        session_file = get_session_file_path()
        login_data = {
            'authenticated': True,
            'username': username,
            'timestamp': str(pd.Timestamp.now())
        }
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(login_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"保存登录状态失败: {e}")
        return False

def load_login_state():
    """从持久化文件加载登录状态"""
    try:
        session_file = get_session_file_path()
        if os.path.exists(session_file):
            with open(session_file, 'r', encoding='utf-8') as f:
                login_data = json.load(f)
            
            # 检查文件是否过期(24小时)
            import pandas as pd
            if 'timestamp' in login_data:
                saved_time = pd.Timestamp(login_data['timestamp'])
                current_time = pd.Timestamp.now()
                if (current_time - saved_time).total_seconds() > 24 * 3600:
                    # 文件过期，删除
                    clear_login_state()
                    return None
            
            return login_data
    except Exception as e:
        # 如果文件损坏，清除它
        clear_login_state()
        return None

def clear_login_state():
    """清除登录状态文件"""
    try:
        session_file = get_session_file_path()
        if os.path.exists(session_file):
            os.remove(session_file)
    except Exception:
        pass

def login_page():
    """登录页面"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🤖 AI-CodeReview 代码审查仪表板</h1>
        <p>请输入您的登录凭据</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 用户名")
            password = st.text_input("🔒 密码", type="password")
            submitted = st.form_submit_button("🚪 登录", use_container_width=True)
        
        if submitted:
            if authenticate(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                
                # 保存登录状态
                save_login_state(username)
                
                # 设置URL参数以支持session持久化
                st.query_params["auto_login"] = "true"
                st.query_params["user"] = username
                
                st.success("✅ 登录成功！")
                st.rerun()
            else:
                st.error("❌ 用户名或密码错误！")

def user_menu():
    """用户菜单组件"""
    if "username" in st.session_state:
        # 创建一个不可见的容器来放置用户菜单
        col1, col2 = st.columns([5, 1])
        with col2:
            # 使用popover显示用户菜单
            with st.popover(f"👤 {st.session_state['username']}", help="用户菜单"):
                if st.button("🚪 注销登录", use_container_width=True, key="logout_user_menu"):
                    st.session_state["authenticated"] = False
                    st.session_state.pop("username", None)
                    
                    # 清理URL参数
                    if "auto_login" in st.query_params:
                        del st.query_params["auto_login"]
                    if "user" in st.query_params:
                        del st.query_params["user"]
                    
                    # 清除登录状态
                    clear_login_state()
                    
                    st.rerun()

def check_authentication():
    """检查认证状态"""
    # 初始化session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    
    # 初始化session计数器以支持页面刷新后的状态恢复
    if "session_counter" not in st.session_state:
        st.session_state["session_counter"] = 0
    st.session_state["session_counter"] += 1
    
    # 尝试从持久化文件恢复登录状态（页面刷新后保持登录）
    if not st.session_state["authenticated"]:
        # 先尝试从URL参数恢复
        query_params = st.query_params
        
        restored = False
        
        # 方法1：从URL参数恢复
        if "auto_login" in query_params and query_params["auto_login"] == "true" and "user" in query_params:
            username = query_params["user"]
            if username:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                restored = True
        
        # 方法2：从持久化文件恢复
        if not restored:
            saved_state = load_login_state()
            if saved_state and saved_state.get('authenticated'):
                username = saved_state.get('username')
                if username:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    restored = True
        
        # 如果成功恢复，刷新页面以更新UI
        if restored:
            st.rerun()
    
    return st.session_state["authenticated"]
