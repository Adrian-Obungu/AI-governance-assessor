# export_manager.py - FIXED VERSION
import streamlit as st
import pandas as pd
import json
import base64
import io
from datetime import datetime
from typing import Dict, Any, List

class ProductionExportManager:
    """
    Enterprise-grade export functionality for AI Governance assessments
    """
    
    def __init__(self):
        self.export_history = []
        self.supported_formats = ['excel', 'json', 'csv', 'pdf']
    
    def export_assessment_data(self, scores: Dict, user_info: Dict, format_type: str) -> Dict:
        """
        Main export function supporting multiple formats
        Returns dict with 'success', 'data', 'filename', 'mime_type'
        """
        try:
            if format_type == 'excel':
                return self._export_to_excel(scores, user_info)
            elif format_type == 'json':
                return self._export_to_json(scores, user_info)
            elif format_type == 'csv':
                return self._export_to_csv(scores, user_info)
            elif format_type == 'pdf':
                return self._export_to_pdf(scores, user_info)
            else:
                return {
                    'success': False,
                    'error': f"Unsupported format: {format_type}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _export_to_excel(self, scores: Dict, user_info: Dict) -> Dict:
        """Export to multi-sheet Excel workbook"""
        try:
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Sheet 1: Executive Summary
                summary_data = self._create_summary_data(scores, user_info)
                df_summary = pd.DataFrame([summary_data])
                df_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
                
                # Sheet 2: Domain Scores
                domains_data = self._create_domains_data(scores)
                if domains_data:
                    df_domains = pd.DataFrame(domains_data)
                    df_domains.to_excel(writer, sheet_name='Domain Scores', index=False)
                
                # Sheet 3: Recommendations
                recommendations_data = self._create_recommendations_data(scores)
                if recommendations_data:
                    df_recommendations = pd.DataFrame(recommendations_data)
                    df_recommendations.to_excel(writer, sheet_name='Recommendations', index=False)
                
                # Sheet 4: Risk Analysis
                risk_data = self._create_risk_data(scores)
                if risk_data:
                    df_risk = pd.DataFrame(risk_data)
                    df_risk.to_excel(writer, sheet_name='Risk Analysis', index=False)
            
            output.seek(0)
            excel_data = output.getvalue()
            
            filename = f"AI_Governance_Assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            
            # Log export
            self._log_export('excel', filename, True)
            
            return {
                'success': True,
                'data': excel_data,
                'filename': filename,
                'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
            
        except Exception as e:
            self._log_export('excel', '', False, str(e))
            return {
                'success': False,
                'error': f"Excel export failed: {str(e)}"
            }
    
    def _create_summary_data(self, scores: Dict, user_info: Dict) -> Dict:
        """Create executive summary data"""
        overall = scores.get('overall', {})
        domains = scores.get('domains', {})
        
        # Calculate risk profile
        high_risk = sum(1 for domain in domains.values() if domain.get('raw_percentage', 0) < 40)
        medium_risk = sum(1 for domain in domains.values() if 40 <= domain.get('raw_percentage', 0) < 70)
        
        return {
            'Organization': user_info.get('organization', 'Unknown'),
            'Industry': user_info.get('industry', 'Unknown'),
            'Organization Size': user_info.get('size', 'Unknown'),
            'Region': user_info.get('region', 'Unknown'),
            'Assessment Date': datetime.now().strftime('%Y-%m-%d'),
            'Overall Score': overall.get('percentage', 0),
            'Maturity Level': overall.get('maturity_level', 'Unknown'),
            'Industry Benchmark': overall.get('industry_benchmark', 65),
            'Questions Answered': overall.get('questions_answered', 0),
            'Total Questions': overall.get('total_questions', 0),
            'Completion Rate': f"{(overall.get('questions_answered', 0) / overall.get('total_questions', 1)) * 100:.1f}%",
            'High Risk Domains': high_risk,
            'Medium Risk Domains': medium_risk,
            'Low Risk Domains': len(domains) - high_risk - medium_risk,
            'Overall Risk Profile': 'Critical' if high_risk > len(domains)/2 else 'Elevated' if high_risk > 0 else 'Moderate' if medium_risk > 0 else 'Low'
        }
    
    def _create_domains_data(self, scores: Dict) -> List[Dict]:
        """Create domain scores data"""
        domains_data = []
        for domain_id, domain in scores.get('domains', {}).items():
            score = domain.get('raw_percentage', 0)
            domains_data.append({
                'Domain ID': domain_id,
                'Domain Name': domain.get('name', 'Unknown'),
                'Description': domain.get('description', ''),
                'Score (%)': score,
                'Raw Score': domain.get('raw_score', 0),
                'Max Possible Score': domain.get('max_raw_score', 0),
                'Maturity Level': domain.get('maturity_level', 'Unknown'),
                'Risk Level': 'High' if score < 40 else 'Medium' if score < 70 else 'Low',
                'Questions Answered': domain.get('questions_answered', 0),
                'Total Questions': domain.get('total_questions', 0),
                'Weight': domain.get('weight', 0),
                'Weighted Score': domain.get('weighted_score', 0)
            })
        return domains_data
    
    def _create_recommendations_data(self, scores: Dict) -> List[Dict]:
        """Create recommendations data"""
        recommendations_data = []
        for rec in scores.get('recommendations', []):
            recommendations_data.append({
                'Priority': rec.get('priority', 'medium').upper(),
                'Domain': rec.get('domain', 'General'),
                'Recommendation': rec.get('text', ''),
                'Timeline': rec.get('timeline', 'Not specified'),
                'Impact': rec.get('impact', 'Medium')
            })
        return recommendations_data
    
    def _create_risk_data(self, scores: Dict) -> List[Dict]:
        """Create risk analysis data"""
        risk_data = []
        for domain_id, domain in scores.get('domains', {}).items():
            score = domain.get('raw_percentage', 0)
            risk_data.append({
                'Domain': domain.get('name', 'Unknown'),
                'Score (%)': score,
                'Risk Category': 'High' if score < 40 else 'Medium' if score < 70 else 'Low',
                'Mitigation Priority': 'Immediate' if score < 40 else 'Short-term' if score < 70 else 'Long-term',
                'Benchmark Gap': f"{score - 70:+.1f}%",
                'Improvement Urgency': 'Critical' if score < 40 else 'High' if score < 50 else 'Medium' if score < 70 else 'Low'
            })
        return risk_data
    
    def _export_to_json(self, scores: Dict, user_info: Dict) -> Dict:
        """Export to JSON format"""
        try:
            export_data = {
                'metadata': {
                    'export_timestamp': datetime.now().isoformat(),
                    'export_version': '2.0',
                    'tool': 'AI Governance Pro'
                },
                'organization_info': user_info,
                'assessment_results': scores,
                'summary': self._create_summary_data(scores, user_info)
            }
            
            json_data = json.dumps(export_data, indent=2, default=str)
            filename = f"AI_Governance_Assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            self._log_export('json', filename, True)
            
            return {
                'success': True,
                'data': json_data,
                'filename': filename,
                'mime_type': 'application/json'
            }
            
        except Exception as e:
            self._log_export('json', '', False, str(e))
            return {
                'success': False,
                'error': f"JSON export failed: {str(e)}"
            }
    
    def _export_to_csv(self, scores: Dict, user_info: Dict) -> Dict:
        """Export domain scores to CSV"""
        try:
            domains_data = self._create_domains_data(scores)
            if not domains_data:
                return {
                    'success': False,
                    'error': "No domain data available for CSV export"
                }
            
            df = pd.DataFrame(domains_data)
            csv_data = df.to_csv(index=False)
            filename = f"Domain_Scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            
            self._log_export('csv', filename, True)
            
            return {
                'success': True,
                'data': csv_data,
                'filename': filename,
                'mime_type': 'text/csv'
            }
            
        except Exception as e:
            self._log_export('csv', '', False, str(e))
            return {
                'success': False,
                'error': f"CSV export failed: {str(e)}"
            }
    
    def _export_to_pdf(self, scores: Dict, user_info: Dict) -> Dict:
        """Export to PDF format (placeholder for future implementation)"""
        return {
            'success': False,
            'error': "PDF export is currently in development. Please use Excel or JSON export for now.",
            'available_formats': ['excel', 'json', 'csv']
        }
    
    def _log_export(self, format_type: str, filename: str, success: bool, error: str = ""):
        """Log export operations for auditing"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'format': format_type,
            'filename': filename,
            'success': success,
            'error': error
        }
        self.export_history.append(log_entry)
    
    def get_export_stats(self) -> Dict:
        """Get export statistics"""
        total = len(self.export_history)
        successful = sum(1 for entry in self.export_history if entry['success'])
        failed = total - successful
        
        format_stats = {}
        for entry in self.export_history:
            format_type = entry['format']
            if format_type not in format_stats:
                format_stats[format_type] = {'success': 0, 'failed': 0}
            if entry['success']:
                format_stats[format_type]['success'] += 1
            else:
                format_stats[format_type]['failed'] += 1
        
        return {
            'total_exports': total,
            'successful_exports': successful,
            'failed_exports': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'format_breakdown': format_stats
        }

# Global instance
export_manager = ProductionExportManager()
# ============================================================================
# BACKWARD COMPATIBILITY WRAPPER (Auto-added via terminal fix)
# Date: $(date)
# ============================================================================
def export_user_data(scores, user_info, format_type='json'):
    """
    Legacy function wrapper for ProductionExportManager
    Maintains compatibility with existing import statements in __init__.py
    """
    exporter = ProductionExportManager()
    return exporter.export_assessment_data(scores, user_info, format_type)

# BACKWARD COMPATIBILITY WRAPPER (Auto-added)
def export_user_data(scores, user_info, format_type="json"):
    """Legacy wrapper for ProductionExportManager"""
    exporter = ProductionExportManager()
    return exporter.export_assessment_data(scores, user_info, format_type)
