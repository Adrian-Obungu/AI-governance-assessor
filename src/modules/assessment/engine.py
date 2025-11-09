"""Assessment engine"""
import streamlit as st

class AssessmentEngine:
    def render_question(self, question):
        """Render a single assessment question"""
        st.markdown(f"**{question['text']}**")
        
        options = [opt['text'] for opt in question['maturity_levels']]
        current_response = st.session_state.responses.get(question['id'])
        
        selected = st.radio(
            "Select maturity level:",
            options=options,
            index=current_response if current_response is not None else 0,
            key=f"radio_{question['id']}",
            label_visibility="collapsed"
        )
        
        # Save response
        for idx, opt in enumerate(question['maturity_levels']):
            if opt['text'] == selected:
                st.session_state.responses[question['id']] = opt['score']
                break
        
        st.markdown("---")
