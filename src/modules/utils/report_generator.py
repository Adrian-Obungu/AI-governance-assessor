import json
from datetime import datetime

def generate_assessment_report(scores, user_info):
    """Generate assessment report"""
    report = {
        'assessment_date': datetime.now().isoformat(),
        'user_info': user_info,
        'scores': scores,
        'overall_score': scores.get('overall', {}).get('percentage', 0),
        'maturity_level': scores.get('overall', {}).get('maturity_level', 'Unknown')
    }
    return report

def export_to_json(scores, user_info):
    """Export assessment to JSON format"""
    report = generate_assessment_report(scores, user_info)
    return json.dumps(report, indent=2)
