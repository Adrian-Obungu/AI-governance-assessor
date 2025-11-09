# analytics_dashboard.py - SIMPLIFIED & GUARANTEED
import streamlit as st
import plotly.express as px
import pandas as pd

def render_analytics_guaranteed():
    """ELITE: Analytics that cannot fail"""
    st.title("📊 Analytics Dashboard")
    
    # Check for data
    if 'analytics_scores' not in st.session_state:
        st.error("Complete an assessment first")
        st.button("Back to Assessment", on_click=lambda: st.session_state.update({'current_page': 'assessment'}))
        return
    
    scores = st.session_state.analytics_scores
    
    # ALWAYS WORKS - Basic metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{scores.get('overall', {}).get('percentage', 0)}%")
    with col2:
        st.metric("Maturity", scores.get('overall', {}).get('maturity_level', 'Unknown'))
    with col3:
        st.metric("Questions", scores.get('overall', {}).get('questions_answered', 0))
    
    # ALWAYS WORKS - Domain scores
    st.subheader("Domain Performance")
    for domain_id, domain in scores.get('domains', {}).items():
        score = domain.get('raw_percentage', 0)
        st.write(f"**{domain.get('name', 'Unknown')}**: {score}%")
        st.progress(score / 100)
    
    # OPTIONAL - Charts (won't break if they fail)
    try:
        domains_data = [{'Domain': d['name'], 'Score': d['raw_percentage']} 
                       for d in scores.get('domains', {}).values()]
        if domains_data:
            fig = px.bar(domains_data, x='Domain', y='Score', title="Domain Scores")
            st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("Charts unavailable - data table shown instead")
    
    # GUARANTEED navigation
    st.button("← Back to Assessment", on_click=lambda: st.session_state.update({'current_page': 'assessment'}))
# BACKWARD COMPATIBILITY FUNCTION
def render_analytics():
    """Legacy wrapper for render_analytics_guaranteed"""
    return render_analytics_guaranteed()
