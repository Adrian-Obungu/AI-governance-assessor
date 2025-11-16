import sqlite3
import pandas as pd
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path="data/governance_assessments.db"):
        self.db_path = db_path
        self._init_assessment_schema()
    
    def _init_assessment_schema(self):
        """Initialize assessment data tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Assessment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                org_id INTEGER,
                assessment_name TEXT,
                framework_version TEXT,
                overall_score REAL,
                overall_maturity TEXT,
                completion_percentage REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                submitted_at TIMESTAMP,
                status TEXT DEFAULT 'in_progress',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        
        # Database migration: Add org_id if missing
        cursor.execute("PRAGMA table_info(assessments)")
        assessment_columns = [col[1] for col in cursor.fetchall()]
        
        if 'org_id' not in assessment_columns:
            cursor.execute("ALTER TABLE assessments ADD COLUMN org_id INTEGER")
            logger.info("Added org_id column to assessments table")
        
        # Assessment responses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessment_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                question_id TEXT NOT NULL,
                domain_id TEXT NOT NULL,
                response_score INTEGER,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
            )
        """)
        
        # Domain scores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS domain_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                domain_id TEXT NOT NULL,
                domain_name TEXT,
                raw_score REAL,
                max_score REAL,
                percentage REAL,
                maturity_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessments_user_id ON assessments(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessments_org_id ON assessments(org_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessments_created ON assessments(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_responses_assessment ON assessment_responses(assessment_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain_scores_assessment ON domain_scores(assessment_id)")
        
        conn.commit()
        conn.close()
        logger.info("Assessment schema initialized")
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def save_assessment(self, user_id, scores, assessment_name, framework_version="nist_rmf_enhanced"):
        """Save complete assessment with scores and responses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            overall = scores.get('overall', {})
            
            # Insert assessment
            cursor.execute("""
                INSERT INTO assessments (user_id, assessment_name, framework_version, overall_score, 
                                        overall_maturity, completion_percentage, status, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                user_id,
                assessment_name,
                framework_version,
                overall.get('percentage', 0),
                overall.get('maturity_level', 'Unknown'),
                (overall.get('questions_answered', 0) / overall.get('total_questions', 1)) * 100 if overall.get('total_questions', 0) > 0 else 0,
                'submitted'
            ))
            
            assessment_id = cursor.lastrowid
            
            # Insert domain scores
            for domain_id, domain_score in scores.get('domains', {}).items():
                cursor.execute("""
                    INSERT INTO domain_scores (assessment_id, domain_id, domain_name, raw_score, 
                                              max_score, percentage, maturity_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    assessment_id,
                    domain_id,
                    domain_score.get('name', domain_id),
                    domain_score.get('raw_score', 0),
                    domain_score.get('max_score', 0),
                    domain_score.get('raw_percentage', 0),
                    domain_score.get('maturity_level', 'Unknown')
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Assessment {assessment_id} saved for user {user_id}")
            return assessment_id
            
        except Exception as e:
            logger.error(f"Error saving assessment: {str(e)}")
            return None
    
    def save_assessment_responses(self, assessment_id, responses, framework):
        """Save individual question responses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for domain_id, domain_data in framework.items():
                for question in domain_data.get('questions', []):
                    q_id = question['id']
                    if q_id in responses:
                        cursor.execute("""
                            INSERT INTO assessment_responses (assessment_id, question_id, domain_id, response_score)
                            VALUES (?, ?, ?, ?)
                        """, (assessment_id, q_id, domain_id, responses[q_id]))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Assessment responses saved for assessment {assessment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving assessment responses: {str(e)}")
            return False
    
    def get_assessment_history(self, user_id=None, organization_name=None):
        """Get assessment history with filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM assessments WHERE 1=1"
            params = []
            
            if user_id:
                query += " AND user_id=?"
                params.append(user_id)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            assessments = cursor.fetchall()
            conn.close()
            
            return assessments or []
            
        except Exception as e:
            logger.error(f"Error retrieving assessment history: {str(e)}")
            return []
    
    def get_assessment_by_id(self, assessment_id):
        """Get specific assessment with all scores and responses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM assessments WHERE id=?", (assessment_id,))
            assessment = cursor.fetchone()
            
            if not assessment:
                conn.close()
                return None
            
            cursor.execute("SELECT * FROM domain_scores WHERE assessment_id=?", (assessment_id,))
            domain_scores = cursor.fetchall()
            
            cursor.execute("SELECT * FROM assessment_responses WHERE assessment_id=?", (assessment_id,))
            responses = cursor.fetchall()
            
            conn.close()
            
            return {
                'assessment': assessment,
                'domain_scores': domain_scores,
                'responses': responses
            }
            
        except Exception as e:
            logger.error(f"Error retrieving assessment: {str(e)}")
            return None
    
    def export_to_csv(self, assessment_id):
        """Export assessment to CSV format"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT * FROM domain_scores WHERE assessment_id=?"
            df = pd.read_sql_query(query, conn, params=(assessment_id,))
            conn.close()
            return df.to_csv(index=False)
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return None
    
    def get_user_assessments_isolated(self, user_id, org_id):
        """Return assessments for a user, filtered by org_id."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assessments WHERE user_id=? AND org_id=? ORDER BY created_at DESC", (user_id, org_id))
            assessments = cursor.fetchall()
            conn.close()
            return assessments or []
        except Exception as e:
            logger.error(f"Error retrieving isolated assessments: {str(e)}")
            return []

    def get_assessment_by_id_isolated(self, assessment_id, org_id):
        """Return assessment only if it matches org_id."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assessments WHERE id=? AND org_id=?", (assessment_id, org_id))
            assessment = cursor.fetchone()
            if not assessment:
                conn.close()
                return None
            cursor.execute("SELECT * FROM domain_scores WHERE assessment_id=?", (assessment_id,))
            domain_scores = cursor.fetchall()
            cursor.execute("SELECT * FROM assessment_responses WHERE assessment_id=?", (assessment_id,))
            responses = cursor.fetchall()
            conn.close()
            return {
                'assessment': assessment,
                'domain_scores': domain_scores,
                'responses': responses
            }
        except Exception as e:
            logger.error(f"Error retrieving isolated assessment: {str(e)}")
            return None

db_manager = DatabaseManager()
