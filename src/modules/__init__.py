# Modules package initialization
# This file makes the modules directory a Python package

# Import key modules to make them available at the modules level
from .assessment.scoring_engine import calculate_maturity_score
from .utils.report_generator import generate_assessment_report

# Define what's available when importing from modules
__all__ = [
    'calculate_maturity_score',
    'generate_assessment_report'
]
