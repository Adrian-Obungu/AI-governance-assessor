def calculate_maturity_score(responses, framework):
    """Calculate maturity scores based on responses"""
    # Basic implementation - you'll need to expand this
    total_score = 0
    max_score = 0
    
    for domain_id, domain_data in framework['domains'].items():
        for question in domain_data['questions']:
            question_max = max(level['score'] for level in question['maturity_levels'])
            max_score += question_max
            
            if question['id'] in responses and responses[question['id']] is not None:
                total_score += responses[question['id']]
    
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    return {
        'overall': {
            'percentage': overall_percentage,
            'maturity_level': get_maturity_level(overall_percentage)
        }
    }

def get_maturity_level(percentage):
    """Determine maturity level from percentage"""
    if percentage >= 85: return "Advanced"
    elif percentage >= 70: return "Proficient" 
    elif percentage >= 50: return "Developing"
    else: return "Initial"
