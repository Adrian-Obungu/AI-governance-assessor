"""
Data models for AI Governance Assessment Tool.
Clean, error-free implementation.
"""
from enum import Enum
from typing import List, Optional, Any, Dict


class Industry(str, Enum):
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    TECHNOLOGY = "technology"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    GOVERNMENT = "government"
    EDUCATION = "education"
    OTHER = "other"


class CriticalityLevel(str, Enum):
    MISSION_CRITICAL = "High - Mission Critical"
    BUSINESS_CRITICAL = "Medium - Business Operations"
    INTERNAL_TOOL = "Low - Internal Tool"
    EXPERIMENTAL = "Experimental - No Production Impact"


class ModelType(str, Enum):
    LLM_CHATBOT = "LLM Chatbot"
    CLASSIFICATION = "Classification Model"
    REGRESSION = "Regression Model"
    COMPUTER_VISION = "Computer Vision"
    RECOMMENDATION = "Recommendation System"
    GENERATIVE_AI = "Generative AI"
    OTHER = "Other"


class CompanyInfo:
    def __init__(self, industry: Industry, size: str, region: str, compliance_frameworks: List[str]):
        self.industry = industry
        self.size = size
        self.region = region
        self.compliance_frameworks = compliance_frameworks


class UseCase:
    def __init__(self, name: str, model_type: ModelType, criticality: CriticalityLevel, 
                 description: str = "", data_sensitivity: str = "confidential"):
        self.name = name
        self.model_type = model_type
        self.criticality = criticality
        self.description = description
        self.data_sensitivity = data_sensitivity


class Evidence:
    def __init__(self, question_id: str, file_name: str, content: str, analysis: Optional[str] = None):
        self.question_id = question_id
        self.file_name = file_name
        self.content = content
        self.analysis = analysis


class AssessmentContext:
    def __init__(self, company_info: CompanyInfo, use_case: UseCase, 
                 responses: Dict[str, Any], evidence: List[Evidence], timestamp: str):
        self.company_info = company_info
        self.use_case = use_case
        self.responses = responses
        self.evidence = evidence
        self.timestamp = timestamp 