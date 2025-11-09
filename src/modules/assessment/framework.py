"""Assessment framework definitions - Loads from JSON"""
import json
import os

def get_assessment_framework():
    """Load the complete assessment framework from JSON file"""
    framework_path = os.path.join(os.path.dirname(__file__), 'frameworks', 'multi_framework_enhanced.json')
    
    try:
        with open(framework_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Return just the domains section
            return data.get('domains', {})
    except Exception as e:
        # Emergency fallback (should never happen)
        print(f' WARNING: Failed to load framework: {e}')
        return {}
