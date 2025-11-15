"""
THEME-AWARE UI SYSTEM
Enterprise-grade styling that works with Streamlit's theming
"""
import streamlit as st

class ThemeManager:
    def __init__(self):
        self.current_theme = self._detect_theme()
    
    def _detect_theme(self):
        """Detect current Streamlit theme"""
        try:
            # Check if we're in dark mode
            if hasattr(st, 'theme') and st.theme:
                return 'dark' if st.theme.base == 'dark' else 'light'
        except:
            pass
        return 'light'
    
    def get_css_variables(self):
        """Get CSS variables based on current theme"""
        if self.current_theme == 'dark':
            return {
                'text_primary': '#FFFFFF',
                'text_secondary': '#94A3B8',
                'background_primary': '#0F172A',
                'background_secondary': '#1E293B',
                'accent_primary': '#3B82F6',
                'accent_secondary': '#6366F1',
                'border_color': '#334155',
                'success_color': '#10B981',
                'warning_color': '#F59E0B',
                'error_color': '#EF4444'
            }
        else:
            return {
                'text_primary': '#000000',
                'text_secondary': '#6B7280',
                'background_primary': '#FFFFFF',
                'background_secondary': '#F8FAFC',
                'accent_primary': '#2563EB',
                'accent_secondary': '#7C3AED',
                'border_color': '#E5E7EB',
                'success_color': '#059669',
                'warning_color': '#D97706',
                'error_color': '#DC2626'
            }
    
    def apply_theme_styles(self):
        """Apply theme-aware CSS styles"""
        css_vars = self.get_css_variables()
        
        css = f"""
        <style>
        /* CSS Variables for Theme Management */
        :root {{
            --text-primary: {css_vars['text_primary']};
            --text-secondary: {css_vars['text_secondary']};
            --background-primary: {css_vars['background_primary']};
            --background-secondary: {css_vars['background_secondary']};
            --accent-primary: {css_vars['accent_primary']};
            --accent-secondary: {css_vars['accent_secondary']};
            --border-color: {css_vars['border_color']};
            --success-color: {css_vars['success_color']};
            --warning-color: {css_vars['warning_color']};
            --error-color: {css_vars['error_color']};
        }}
        
        /* Base Styles Using CSS Variables */
        .stApp {{
            color: var(--text-primary) !important;
            background-color: var(--background-primary) !important;
        }}
        
        /* Text Elements */
        h1, h2, h3, h4, h5, h6, p, div, span, label {{
            color: var(--text-primary) !important;
        }}
        
        /* Input Elements */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {{
            color: var(--text-primary) !important;
            background-color: var(--background-secondary) !important;
            border-color: var(--border-color) !important;
        }}
        
        /* Buttons */
        .stButton button {{
            color: var(--text-primary) !important;
            background-color: var(--accent-primary) !important;
            border-color: var(--accent-primary) !important;
        }}
        
        /* Cards and Containers */
        .enterprise-card {{
            background: var(--background-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        /* Status Colors */
        .success-text {{ color: var(--success-color) !important; }}
        .warning-text {{ color: var(--warning-color) !important; }}
        .error-text {{ color: var(--error-color) !important; }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    def get_button_style(self, button_type="primary"):
        """Get button style based on type and theme"""
        base_style = {
            "use_container_width": True,
            "type": button_type
        }
        
        # Add unique keys to prevent duplicate ID errors
        import time
        base_style["key"] = f"{button_type}_{int(time.time() * 1000)}"
        
        return base_style

# Global theme manager
theme_manager = ThemeManager()

def render_enterprise_header():
    """Render professional enterprise header"""
    theme_manager.apply_theme_styles()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<div style="text-align: center; font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">🏢 AI Governance Pro</div>',
            unsafe_allow_html=True
        )
        st.caption("Enterprise AI Risk Management Assessment Platform")

def render_value_card(title, description, icon="🛡️"):
    """Render consistent value proposition card"""
    st.markdown(f"""
    <div class="enterprise-card">
        <h4>{icon} {title}</h4>
        <p style="color: var(--text-secondary); margin-bottom: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)
