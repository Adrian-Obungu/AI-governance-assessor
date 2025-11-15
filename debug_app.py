import streamlit as st
import sys
import os

print("DEBUG: Starting diagnostic app...")

# Simple test app
st.set_page_config(page_title="Debug App", layout="wide")
st.title("🔧 AI Governance Pro - Debug Version")
st.write("This is a test to see if basic Streamlit works")

# Test button functionality
if st.button("Test Button 1"):
    st.success("Button 1 worked!")
    
if st.button("Test Button 2"):
    st.error("Button 2 worked!")

# Test session state
if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

if st.button(f"Click Count: {st.session_state.click_count}"):
    st.session_state.click_count += 1
    st.rerun()

st.write("If you can see this text and buttons work, the basic setup is OK")
