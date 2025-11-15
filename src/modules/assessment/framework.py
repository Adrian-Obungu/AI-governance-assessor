"""Assessment framework loader for AI Governance Pro"""
import json
import os

def get_assessment_framework():
    """Load comprehensive assessment framework from JSON"""
    framework_path = os.path.join(os.path.dirname(__file__), 'frameworks', 'nist_rmf_enhanced.json')
    
    try:
        with open(framework_path, 'r', encoding='utf-8') as f:
            framework = json.load(f)
        
        # Validate framework structure
        required_domains = ['governance_strategy', 'risk_management', 'lifecycle_management', 
                           'transparency_explainability', 'compliance_ethics']
        
        for domain in required_domains:
            if domain not in framework:
                raise ValueError(f"Missing domain: {domain}")
        
        total_questions = sum(len(domain_data['questions']) for domain_data in framework.values())
        print(f"✅ Framework loaded: {len(framework)} domains, {total_questions} questions")
        
        return framework
        
    except Exception as e:
        print(f"❌ Error loading framework: {e}")
        # Fallback to minimal framework
        return {
            "governance_strategy": {
                "name": "Governance & Strategy",
                "description": "Executive oversight and policies",
                "questions": [
                    {
                        "id": "GOV_01",
                        "text": "Emergency fallback question",
                        "framework": "Fallback",
                        "maturity_levels": [
                            {"score": 0, "text": "Not started"},
                            {"score": 1, "text": "Initial"},
                            {"score": 2, "text": "Developing"},
                            {"score": 3, "text": "Established"},
                            {"score": 4, "text": "Advanced"},
                            {"score": 5, "text": "Optimized"}
                        ]
                    }
                ]
            }
        }

# Test the framework loader
if __name__ == "__main__":
    framework = get_assessment_framework()
    for domain_id, domain_data in framework.items():
        print(f"  {domain_data['name']}: {len(domain_data['questions'])} questions")
