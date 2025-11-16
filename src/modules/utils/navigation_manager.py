import streamlit as st

class NavigationManager:
    def __init__(self):
        self.pages = {}
        self.current_page = "login"
    
    def register_page(self, page_name, render_function):
        self.pages[page_name] = render_function
    
    def set_current_page(self, page_name):
        self.current_page = page_name
    
    def render_current_page(self):
        if self.current_page in self.pages:
            self.pages[self.current_page]()
        else:
            st.error(f"Page '{self.current_page}' not found")

