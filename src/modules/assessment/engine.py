"""Assessment engine"""
import streamlit as st
from modules.assessment.framework import get_assessment_framework
from modules.assessment.scoring_engine import calculate_maturity_score

class AssessmentEngine:
    def render_question(self, question):
        """Render a single assessment question"""
        st.markdown(f"""**{question["text"]}**""")

        options = [opt["text"] for opt in question["maturity_levels"]]
        current_response = st.session_state.responses.get(question["id"])

        selected = st.radio(
            "Select maturity level:",
            options=options,
            index=current_response if current_response is not None else 0,
            key=f"""radio_{question["id"]}""",
            label_visibility="collapsed"
        )

        # Save response
        for idx, opt in enumerate(question["maturity_levels"]):
            if opt["text"] == selected:
                st.session_state.responses[question["id"]] = opt["score"]
                break

        st.markdown("---")


def render_assessment():
    """Main assessment rendering function"""
    framework = get_assessment_framework()

    st.markdown("""<div class="main-header">AI Governance Pro</div>""", unsafe_allow_html=True)
    st.caption("Enterprise AI Risk Management Assessment")

    # Progress indicator
    total_questions = sum(len(domain["questions"]) for domain in framework.values())
    answered = len([r for r in st.session_state.responses.values() if r is not None])
    progress = answered / total_questions if total_questions > 0 else 0

    st.progress(progress)
    st.markdown(f"""**Progress:** {answered}/{total_questions} answered ({progress:.0%})""")

    # Render questions
    engine = AssessmentEngine()
    for domain_id, domain_data in framework.items():
        with st.expander(f"""{domain_data["name"]}""", expanded=True):
            for question in domain_data["questions"]:
                engine.render_question(question)

    # Submit button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Assessment", type="primary", use_container_width=True):
            scores = calculate_maturity_score(st.session_state.responses)
            st.session_state.assessment_scores = scores
            st.session_state.current_page = "analytics"
            st.success("Assessment submitted!")
            st.rerun()


def show_assessment_results():
    """Display results"""
    if "assessment_scores" not in st.session_state:
        st.warning("No results. Complete an assessment first.")
        return

    scores = st.session_state.assessment_scores
    st.title("📊 Assessment Results")

    # Metrics
    overall = scores.get("overall", {})
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{overall.get("percentage", 0):.1f}%")
    with col2:
        st.metric("Maturity", overall.get("maturity_level", "Unknown"))
    with col3:
        st.metric("Answered", overall.get("questions_answered", 0))

    st.markdown("---")
    st.subheader("Domain Performance")
    for domain_id, domain_score in scores.get("domains", {}).items():
        score = domain_score.get("raw_percentage", 0)
        st.write(f"""**{domain_score["name"]}**: {score:.1f}%""")
        st.progress(score / 100)

    # Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Export", use_container_width=True):
            st.info("Export coming soon!")
    with col2:
        if st.button("🔄 Retake", use_container_width=True):
            st.session_state.responses = {}
            st.session_state.assessment_scores = None
            st.rerun()
    with col3:
        if st.button("🏠 Back", use_container_width=True):
            st.session_state.current_page = "assessment"
            st.rerun()
