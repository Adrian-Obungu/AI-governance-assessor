import streamlit as st
import plotly.graph_objects as go

def display_results_dashboard(assessment_data, user_info=None):
    """Display assessment results with professional analytics"""
    
    if not assessment_data:
        st.error("No assessment data available")
        return
    
    st.header("📊 AI Governance Assessment Results")
    
    # Calculate scores
    domain_scores = {}
    total_score = 0
    total_max_score = 0
    
    for domain, data in assessment_data.items():
        questions = data.get("questions", [])
        domain_score = sum(q.get("score", 0) for q in questions)
        domain_max = len(questions) * 5
        domain_percentage = (domain_score / domain_max) * 100 if domain_max > 0 else 0
        
        domain_scores[domain] = {
            "score": domain_score,
            "max_score": domain_max,
            "percentage": domain_percentage,
            "question_count": len(questions)
        }
        
        total_score += domain_score
        total_max_score += domain_max
    
    overall_percentage = (total_score / total_max_score) * 100 if total_max_score > 0 else 0
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{overall_percentage:.1f}%")
    with col2:
        maturity_level = "Optimized" if overall_percentage >= 80 else "Advanced" if overall_percentage >= 60 else "Established" if overall_percentage >= 40 else "Developing"
        st.metric("Maturity Level", maturity_level)
    with col3:
        total_questions = sum(d["question_count"] for d in domain_scores.values())
        st.metric("Questions Completed", total_questions)
    
    # Domain performance chart
    st.subheader("Domain Performance")
    
    domains = list(domain_scores.keys())
    percentages = [domain_scores[d]["percentage"] for d in domains]
    
    fig = go.Figure(data=[
        go.Bar(name="Domain Scores", x=domains, y=percentages,
               text=[f"{p:.1f}%" for p in percentages],
               textposition="auto")
    ])
    
    fig.update_layout(
        title="AI Governance Maturity by Domain",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown
    st.subheader("Detailed Breakdown")
    
    for domain, scores in domain_scores.items():
        with st.expander(f"{domain} - {scores['percentage']:.1f}%"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Raw Score:** {scores['score']}/{scores['max_score']}")
                st.write(f"**Questions:** {scores['question_count']}")
            with col2:
                st.progress(scores['percentage'] / 100)
    
    # Recommendations
    st.subheader("🎯 Recommendations")
    
    if overall_percentage < 40:
        st.warning("**Focus Area: Foundation Building** - Prioritize establishing basic AI governance policies and risk management frameworks.")
    elif overall_percentage < 70:
        st.info("**Focus Area: Process Maturation** - Enhance existing governance structures with advanced monitoring and optimization.")
    else:
        st.success("**Focus Area: Continuous Improvement** - Maintain leadership position with innovative governance practices and industry leadership.")

# Alias for compatibility
render_analytics = display_results_dashboard
generate_assessment_results = display_results_dashboard
