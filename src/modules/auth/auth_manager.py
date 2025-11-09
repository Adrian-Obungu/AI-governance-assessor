"""Authentication manager"""
import streamlit as st

class AuthManager:
    def __init__(self):
        self.users = {
            'user@demo.com': {'password': 'demo', 'name': 'Demo User', 'organization': 'Demo Corp', 'role': 'user'},
            'admin@demo.com': {'password': 'demo', 'name': 'Admin User', 'organization': 'Demo Corp', 'role': 'admin'}
        }
    
    def authenticate(self, email, password):
        """Authenticate user"""
        if email in self.users and self.users[email]['password'] == password:
            return {
                'id': 1,
                'email': email,
                'name': self.users[email]['name'],
                'organization': self.users[email]['organization'],
                'role': self.users[email]['role']
            }
        return None

auth_manager = AuthManager()
