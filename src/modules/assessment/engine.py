"""Assessment engine for AI Governance Pro"""
import streamlit as st
from modules.utils.session_manager import session_manager
from modules.assessment.framework import get_assessment_framework
from modules.assessment.scoring_engine import calculate_maturity_score


class AssessmentEngine:
    def render_question(self, question):
        """Render a single assessment question"""
        st.markdown(f"**{question['text']}**")
        st.caption(f"Framework: {question.get('framework', 'NIST AI RMF')}")
        
        options = [opt["text"] for opt in question["maturity_levels"]]
        current_response = st.session_state.responses.get(question["id"])
        
        selected = st.radio(
            "Select maturity level:",
            options=options,
            index=current_response if current_response is not None else 0,
            key=f"radio_{question['id']}",
            label_visibility="collapsed"
        )
        
        # Save response
        for idx, opt in enumerate(question["maturity_levels"]):
            if opt["text"] == selected:
                st.session_state.responses[question["id"]] = opt["score"]
                break
        
        st.markdown("---")


def render_assessment():
    """Render assessment with session management"""
    # Initialize session state for responses
    if "responses" not in st.session_state:
        st.session_state.responses = {}

    if not st.session_state.get("logged_in"):
        return
    """Main assessment rendering function"""
    framework = get_assessment_framework()
    
    # Header with navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #2563eb, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Governance Pro</div>', unsafe_allow_html=True)
        st.caption("Enterprise AI Risk Management Assessment")
    
    # Progress indicator
    total_questions = sum(len(domain["questions"]) for domain in framework.values())
    answered = len([r for r in st.session_state.responses.values() if r is not None])
    progress = answered / total_questions if total_questions > 0 else 0
    
    st.progress(progress)
    st.markdown(f"**Progress: {answered}/{total_questions} answered ({progress:.0%})**")
    
    # Navigation and logout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.responses = {}
            st.session_state.current_page = "assessment"
            st.rerun()
    
    with col3:
        if st.button("📊 View Results", use_container_width=True, type="secondary"):
            if answered > 0:
                st.session_state.current_page = "analytics"
                st.rerun()
            else:
                st.warning("Complete at least one question to view results")
    
    st.markdown("---")
    
    # Render questions
    engine = AssessmentEngine()
    for domain_id, domain_data in framework.items():
        with st.expander(f"**{domain_data['name']}** - {domain_data['description']}", expanded=True):
            for question in domain_data["questions"]:
                engine.render_question(question)
    
    # Submit button (only show if questions answered)
    if answered > 0:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Submit Assessment", type="primary", use_container_width=True):
                # Calculate scores
                scores = calculate_maturity_score(st.session_state.responses, framework)
                st.session_state.assessment_scores = scores
                st.session_state.current_page = "analytics"
                st.success("Assessment submitted successfully!")
                st.rerun()


def show_assessment_results():
    """Display assessment results with navigation"""
    if "assessment_scores" not in st.session_state:
        st.warning("No assessment results found. Complete an assessment first.")
        if st.button("📝 Take Assessment"):
            st.session_state.current_page = "assessment"
            st.rerun()
        return
    
    scores = st.session_state.assessment_scores
    
    # Header with navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #2563eb, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Assessment Results</div>', unsafe_allow_html=True)
    
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.responses = {}
            st.session_state.assessment_scores = None
            st.rerun()
    
    with col3:
        if st.button("📝 Retake", use_container_width=True):
            st.session_state.responses = {}
            st.session_state.assessment_scores = None
            st.session_state.current_page = "assessment"
            st.rerun()
    
    st.markdown("---")
    
    # Overall metrics
    if scores is None:
        st.error("No assessment data available. Please complete the assessment first.")
        return
    overall = scores.get('overall', {})
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{overall.get('percentage', 0):.1f}%")
    with col2:
        st.metric("Maturity Level", overall.get('maturity_level', 'Unknown'))
    with col3:
        st.metric("Questions Answered", overall.get('questions_answered', 0))
    with col4:
        st.metric("Domains Assessed", overall.get('domains_assessed', 0))
    
    st.markdown("---")
    
    # Domain breakdown
    st.subheader("Domain Performance")
    domains = scores.get('domains', {})
    
    for domain_id, domain_data in domains.items():
        score = domain_data.get('raw_percentage', 0)
        st.write(f"**{domain_data['name']}** - {score:.1f}%")
        st.progress(score / 100)
        st.caption(f"Maturity: {domain_data.get('maturity_level', 'Unknown')}")
        st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Export Report", use_container_width=True):
            st.info("Export functionality coming soon!")
    with col2:
        if st.button("🔄 New Assessment", use_container_width=True):
            st.session_state.responses = {}
            st.session_state.assessment_scores = None
            st.session_state.current_page = "assessment"
            st.rerun()
    with col3:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_page = "analytics"
            st.rerun()


def apply_user_limitations(framework, user_limitations):
    if not user_limitations or "max_questions" not in user_limitations:
        return framework
    max_questions = user_limitations["max_questions"]
    limited_framework = {}
    total_questions = 0
    for domain, domain_data in framework.items():
        limited_domain = domain_data.copy()
        questions = domain_data.get("questions", [])
        if total_questions >= max_questions:
            limited_domain["questions"] = []
        else:
            remaining_slots = max_questions - total_questions
            limited_domain["questions"] = questions[:remaining_slots]
            total_questions += len(limited_domain["questions"])
        limited_framework[domain] = limited_domain
    return limited_framework


def apply_user_limitations(framework, limitations):
    """Apply user question limitations"""
    if not limitations or "max_questions" not in limitations:
        return framework
    
    max_q = limitations["max_questions"]
    limited = {}
    count = 0
    
    for domain, data in framework.items():
        limited_domain = data.copy()
        questions = data.get("questions", [])
        
        if count >= max_q:
            limited_domain["questions"] = []
        else:
            remaining = max_q - count
            limited_domain["questions"] = questions[:remaining]
            count += len(limited_domain["questions"])
        
        limited[domain] = limited_domain
    
    return limited

def render_assessment_ui(framework):
    """Render the assessment UI with all questions"""
    import streamlit as st
    
    if not framework:
        st.error("No assessment framework loaded")
        return None
    
    assessment_data = {}
    question_count = 0
    
    # Calculate total questions for progress
    total_questions = sum(len(domain.get("questions", [])) for domain in framework.values())
    
    # Create progress bar
    progress_bar = st.progress(0)
    
    for domain_name, domain_data in framework.items():
        assessment_data[domain_name] = {
            "title": domain_data.get("title", domain_name),
            "description": domain_data.get("description", ""),
            "questions": []
        }
        
        st.header(f"🎯 {domain_data.get('title', domain_name)}")
        st.write(domain_data.get("description", ""))
        
        questions = domain_data.get("questions", [])
        for i, question in enumerate(questions):
            question_count += 1
            progress = question_count / total_questions if total_questions > 0 else 0
            progress_bar.progress(progress)
            
            st.subheader(f"Question {question_count}/{total_questions}")
            st.write(question.get("text", ""))
            
            # Render options based on question type
            options = question.get("options", [])
            if options:
                selected_option = st.radio(
                    f"Select your maturity level for: {question.get('text', '')}",
                    options,
                    key=f"{domain_name}_q{i}"
                )
                
                # Map selection to score (0-5)
                score_map = {
                    "Not Started": 0,
                    "Initial": 1, 
                    "Developing": 2,
                    "Established": 3,
                    "Advanced": 4,
                    "Optimized": 5
                }
                
                score = score_map.get(selected_option, 0)
                
                # Store the question response
                assessment_data[domain_name]["questions"].append({
                    "text": question.get("text", ""),
                    "options": options,
                    "selected": selected_option,
                    "score": score,
                    "framework": question.get("framework", "NIST RMF")
                })
            else:
                # Default maturity scale
                maturity_level = st.select_slider(
                    f"Rate your maturity for: {question.get('text', '')}",
                    options=["Not Started", "Initial", "Developing", "Established", "Advanced", "Optimized"],
                    value="Not Started",
                    key=f"{domain_name}_q{i}"
                )
                
                score_map = {
                    "Not Started": 0,
                    "Initial": 1, 
                    "Developing": 2,
                    "Established": 3,
                    "Advanced": 4,
                    "Optimized": 5
                }
                
                score = score_map.get(maturity_level, 0)
                
                assessment_data[domain_name]["questions"].append({
                    "text": question.get("text", ""),
                    "selected": maturity_level,
                    "score": score,
                    "framework": question.get("framework", "NIST RMF")
                })
            
            st.markdown("---")
    
    # Complete progress bar
    progress_bar.progress(1.0)
    
    return assessment_data

def calculate_maturity_score(assessment_data, framework):
    """Calculate maturity scores from assessment data"""
    if not assessment_data:
        return None
    
    domain_scores = {}
    total_score = 0
    total_max_score = 0
    
    for domain, data in assessment_data.items():
        questions = data.get("questions", [])
        domain_score = sum(q.get("score", 0) for q in questions)
        domain_max = len(questions) * 5  # 5-point scale
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
    
    return {
        "overall": {
            "score": total_score,
            "max_score": total_max_score,
            "percentage": overall_percentage
        },
        "domains": domain_scores
    }
