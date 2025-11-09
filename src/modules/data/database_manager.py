import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="governance_assessments.db"):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def save_assessment(self, user_info, scores, assessment_name, user_id=None):
        return 1  # mock assessment ID
    
    def get_assessment_history(self, user_id=None, organization_name=None):
        return []

db_manager = DatabaseManager()
