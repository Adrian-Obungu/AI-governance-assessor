def calculate_maturity_score(responses, framework):
    """Calculate maturity scores based on framework and responses"""
    total_score = 0
    max_possible_score = 0
    domain_scores = {}
    
    # Framework is a flat dict: {domain_id: domain_data}
    for domain_id, domain_data in framework.items():
        domain_total = 0
        domain_max = 0
        questions_answered = 0
        
        for question in domain_data.get('questions', []):
            q_id = question['id']
            # Get maturity levels to determine max score
            maturity_levels = question.get('maturity_levels', [])
            if maturity_levels:
                q_max = max(level.get('score', 0) for level in maturity_levels)
            else:
                q_max = 5  # Default max
            
            domain_max += q_max
            
            # Get user's response
            if q_id in responses and responses[q_id] is not None:
                domain_total += responses[q_id]
                questions_answered += 1
                total_score += responses[q_id]
                max_possible_score += q_max
        
        # Calculate domain percentage
        domain_percentage = (domain_total / domain_max * 100) if domain_max > 0 else 0
        
        domain_scores[domain_id] = {
            'name': domain_data.get('name', domain_id),
            'raw_score': domain_total,
            'max_score': domain_max,
            'raw_percentage': domain_percentage,
            'questions_answered': questions_answered,
            'maturity_level': get_maturity_level(domain_percentage)
        }
    
    # Overall score
    overall_percentage = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0
    
    overall = {
        'raw_score': total_score,
        'max_score': max_possible_score,
        'percentage': overall_percentage,
        'questions_answered': len(responses),
        'maturity_level': get_maturity_level(overall_percentage)
    }
    
    return {
        'overall': overall,
        'domains': domain_scores
    }

    


def get_maturity_level(percentage):
    """
    Convert percentage to maturity level (0-5 scale)
    
    Maturity Scale:
    - 0-15%: Not Started (no capability)
    - 16-30%: Initial (ad-hoc/reactive)
    - 31-50%: Developing (basic/planned)
    - 51-75%: Established (managed/defined)
    - 76-90%: Advanced (measured/integrated)
    - 91-100%: Optimized (continuous/optimized)
    
    Args:
        percentage: Score percentage (0-100)
        
    Returns:
        str: Maturity level name
    """
    if percentage >= 91:
        return 'Optimized'
    elif percentage >= 76:
        return 'Advanced'
    elif percentage >= 51:
        return 'Established'
    elif percentage >= 31:
        return 'Developing'
    elif percentage >= 16:
        return 'Initial'
    else:
        return 'Not Started'
