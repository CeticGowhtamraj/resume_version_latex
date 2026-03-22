"""
ML Predictions Module
Loads trained models and makes predictions on new resumes
"""

import pickle
import numpy as np
import pandas as pd
import os
import warnings

try:
    from sklearn.exceptions import InconsistentVersionWarning
except Exception:
    InconsistentVersionWarning = None

class ResumeMLPredictor:
    """ML-powered resume predictions"""
    
    def __init__(self, models_dir='models'):
        """Load all trained models"""
        self.models_dir = models_dir
        self.models_loaded = False
        
        try:
            if InconsistentVersionWarning is not None:
                warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

            # Load all models
            with open(f'{models_dir}/ats_score_model.pkl', 'rb') as f:
                self.ats_score_model = pickle.load(f)
            
            with open(f'{models_dir}/job_role_model.pkl', 'rb') as f:
                self.job_role_model = pickle.load(f)
            
            with open(f'{models_dir}/experience_level_model.pkl', 'rb') as f:
                self.experience_level_model = pickle.load(f)
            
            with open(f'{models_dir}/fraud_detection_model.pkl', 'rb') as f:
                self.fraud_detection_model = pickle.load(f)
            
            with open(f'{models_dir}/quality_tier_model.pkl', 'rb') as f:
                self.quality_tier_model = pickle.load(f)
            
            # Load preprocessing objects
            with open(f'{models_dir}/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            
            with open(f'{models_dir}/encoders.pkl', 'rb') as f:
                encoders = pickle.load(f)
                self.role_encoder = encoders['role_encoder']
                self.experience_encoder = encoders['experience_encoder']
                self.quality_encoder = encoders['quality_encoder']
            
            with open(f'{models_dir}/feature_columns.pkl', 'rb') as f:
                self.feature_columns = pickle.load(f)
            
            self.models_loaded = True
            print("[OK] ML Models loaded successfully")
            
        except Exception as e:
            print(f"[WARN] Could not load ML models: {str(e)}")
            print("[WARN] Common cause: scikit-learn version mismatch with saved model files.")
            print("[WARN] Fix by installing requirements (scikit-learn==1.5.2) or retraining models.")
            print("       Falling back to rule-based predictions")
            self.models_loaded = False
    
    def extract_ml_features(self, resume_data, resume_text):
        """
        Extract features from resume data for ML prediction
        
        Args:
            resume_data: Dictionary with parsed resume information
            resume_text: Raw resume text
        
        Returns:
            Dictionary of features
        """
        text_lower = resume_text.lower()
        
        # Basic features
        skills_count = len(resume_data.get('skills', []))
        experience_years = resume_data.get('experience_years', 0)
        
        # Professional links
        has_linkedin = 1 if 'linkedin' in text_lower else 0
        has_github = 1 if 'github' in text_lower else 0
        has_portfolio = 1 if any(word in text_lower for word in ['portfolio', 'website', 'behance']) else 0
        
        # Professional summary
        summary_keywords = ['summary', 'objective', 'profile', 'about me']
        has_summary = 1 if any(word in text_lower for word in summary_keywords) else 0
        
        import re
        summary_pattern = r'(?:summary|objective|profile|about me)[\s:]*([^\n]{40,})'
        summary_match = re.search(summary_pattern, text_lower, re.IGNORECASE)
        summary_length = len(summary_match.group(1)) if summary_match else 0
        
        # Projects
        project_keywords = ['project', 'projects', 'built', 'developed', 'created']
        project_count = sum(1 for keyword in project_keywords if keyword in text_lower)
        project_count = min(project_count, 10)  # Cap at 10
        
        # Education
        education_keywords = ['education', 'degree', 'university', 'bachelor', 'master']
        has_education = 1 if any(word in text_lower for word in education_keywords) else 0
        
        education_score = 0
        if has_education:
            education_pattern = r'(?:bachelor|master|b\.tech|degree).*?(\d{4})'
            if re.search(education_pattern, text_lower):
                education_score = 10
            else:
                education_score = 7
        else:
            education_score = 3
        
        # Page count
        page_count = resume_data.get('no_of_pages', 1)
        
        # Action verbs
        action_verbs = [
            'led', 'managed', 'developed', 'created', 'implemented', 'designed',
            'built', 'increased', 'improved', 'achieved', 'delivered', 'launched',
            'optimized', 'automated'
        ]
        action_verbs_count = sum(1 for verb in action_verbs if verb in text_lower)
        
        # Metrics (quantifiable achievements)
        metrics_patterns = [
            r'\d+%',  # Percentages
            r'\$\d+',  # Money
            r'\d+x',  # Multiples
            r'\d+\s*(?:users|customers|clients)',
            r'\d+\s*(?:projects|applications)',
        ]
        metrics_count = sum(1 for pattern in metrics_patterns if re.search(pattern, text_lower))
        
        # Role-specific keywords
        role_keywords_map = {
            'data scientist': ['python', 'machine learning', 'tensorflow', 'pytorch', 'data science'],
            'data analyst': ['sql', 'excel', 'tableau', 'power bi', 'analytics'],
            'data engineer': ['spark', 'hadoop', 'etl', 'pipeline', 'kafka'],
            'software engineer': ['java', 'python', 'algorithm', 'api', 'git'],
            'web developer': ['html', 'css', 'javascript', 'react', 'node'],
            'mobile developer': ['android', 'ios', 'kotlin', 'swift', 'flutter'],
            'ui/ux designer': ['figma', 'sketch', 'adobe', 'wireframe', 'prototyping'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'aws', 'terraform']
        }
        
        role_keywords_count = 0
        for role_keywords in role_keywords_map.values():
            role_keywords_count += sum(1 for keyword in role_keywords if keyword in text_lower)
        
        # Work experience dates
        year_matches = len(re.findall(r'\b(19|20)\d{2}\b', resume_text))
        work_experience_dates_count = min(year_matches // 2, 10)  # Estimate pairs of dates
        
        # Certifications
        cert_keywords = ['certified', 'certification', 'certificate']
        certification_count = sum(1 for keyword in cert_keywords if keyword in text_lower)
        
        # Skills per project ratio
        skills_per_project = skills_count / max(project_count, 1)
        
        # Context validation score (simplified)
        context_validation_score = min(100, 
            (action_verbs_count * 5 + metrics_count * 8 + project_count * 7))
        
        # Achievements
        has_achievements = 1 if metrics_count > 0 else 0
        
        # Engineered features
        profile_completeness = (has_linkedin + has_github + has_portfolio + has_summary) / 4 * 100
        exp_skills_ratio = experience_years / (skills_count + 1)
        project_engagement = (project_count * metrics_count * (action_verbs_count + 1)) / 100
        quality_score = action_verbs_count * 2 + metrics_count * 3 + has_achievements * 10
        exp_authenticity = (work_experience_dates_count / (experience_years + 1)) * 10
        skill_validation = (context_validation_score * project_count) / (skills_count + 1)
        
        # Create features dictionary
        features = {
            'skills_count': skills_count,
            'experience_years': experience_years,
            'has_linkedin': has_linkedin,
            'has_github': has_github,
            'has_portfolio': has_portfolio,
            'has_summary': has_summary,
            'summary_length': summary_length,
            'project_count': project_count,
            'education_score': education_score,
            'page_count': page_count,
            'action_verbs_count': action_verbs_count,
            'metrics_count': metrics_count,
            'role_keywords_count': role_keywords_count,
            'work_experience_dates_count': work_experience_dates_count,
            'certification_count': certification_count,
            'skills_per_project': skills_per_project,
            'context_validation_score': context_validation_score,
            'has_achievements': has_achievements,
            # Engineered features
            'profile_completeness': profile_completeness,
            'exp_skills_ratio': exp_skills_ratio,
            'project_engagement': project_engagement,
            'quality_score': quality_score,
            'exp_authenticity': exp_authenticity,
            'skill_validation': skill_validation
        }
        
        return features
    
    def predict_ats_score(self, features_dict):
        """Predict ATS score using ML model"""
        if not self.models_loaded:
            return None, 0
        
        try:
            # Convert to DataFrame with correct column order
            X = pd.DataFrame([features_dict])[self.feature_columns]
            
            # Predict
            score = self.ats_score_model.predict(X)[0]
            score = max(0, min(100, int(round(score))))
            
            # Get confidence (using model's score if available)
            if hasattr(self.ats_score_model, 'score'):
                confidence = 95  # High confidence for well-trained model
            else:
                confidence = 90
            
            return score, confidence
            
        except Exception as e:
            print(f"Error in ATS prediction: {str(e)}")
            return None, 0
    
    def predict_job_role(self, features_dict):
        """Predict job role using ML model"""
        if not self.models_loaded:
            return None, 0
        
        try:
            X = pd.DataFrame([features_dict])[self.feature_columns]
            
            # Predict
            role_encoded = self.job_role_model.predict(X)[0]
            role = self.role_encoder.inverse_transform([role_encoded])[0]
            
            # Get probability/confidence
            if hasattr(self.job_role_model, 'predict_proba'):
                proba = self.job_role_model.predict_proba(X)[0]
                confidence = int(max(proba) * 100)
            else:
                confidence = 85
            
            return role, confidence
            
        except Exception as e:
            print(f"Error in role prediction: {str(e)}")
            return None, 0
    
    def predict_experience_level(self, features_dict):
        """Predict experience level using ML model"""
        if not self.models_loaded:
            return None, 0
        
        try:
            X = pd.DataFrame([features_dict])[self.feature_columns]
            
            exp_encoded = self.experience_level_model.predict(X)[0]
            exp_level = self.experience_encoder.inverse_transform([exp_encoded])[0]
            
            # Get confidence
            if hasattr(self.experience_level_model, 'predict_proba'):
                proba = self.experience_level_model.predict_proba(X)[0]
                confidence = int(max(proba) * 100)
            else:
                confidence = 95  # High confidence due to good accuracy
            
            return exp_level, confidence
            
        except Exception as e:
            print(f"Error in experience prediction: {str(e)}")
            return None, 0
    
    def predict_fraud(self, features_dict):
        """Predict if resume is fraudulent using ML model"""
        if not self.models_loaded:
            return None, 0, {}
        
        try:
            X = pd.DataFrame([features_dict])[self.feature_columns]
            
            # Check if model needs scaled features
            if hasattr(self.fraud_detection_model, 'coef_'):  # Logistic Regression
                X_scaled = self.scaler.transform(X)
                is_fraud = self.fraud_detection_model.predict(X_scaled)[0]
                
                if hasattr(self.fraud_detection_model, 'predict_proba'):
                    proba = self.fraud_detection_model.predict_proba(X_scaled)[0]
                    confidence = int(max(proba) * 100)
                else:
                    confidence = 90
            else:  # Tree-based models
                is_fraud = self.fraud_detection_model.predict(X)[0]
                
                if hasattr(self.fraud_detection_model, 'predict_proba'):
                    proba = self.fraud_detection_model.predict_proba(X)[0]
                    confidence = int(max(proba) * 100)
                else:
                    confidence = 95
            
            # Calculate authenticity score (inverse of fraud)
            authenticity_score = 100 - (is_fraud * 100)
            
            # Determine risk level and verdict
            if is_fraud == 1:
                if confidence >= 95:
                    risk_level = "Critical"
                    verdict = "❌ VERY HIGH RISK - Likely fraud"
                else:
                    risk_level = "High"
                    verdict = "🚨 HIGH RISK - Possible fraud"
            else:
                if confidence >= 95:
                    risk_level = "Low"
                    verdict = "✅ HIGHLY AUTHENTIC"
                else:
                    risk_level = "Low-Medium"
                    verdict = "✓ LIKELY AUTHENTIC"
            
            result = {
                'is_fraud': bool(is_fraud),
                'authenticity_score': authenticity_score,
                'confidence': confidence,
                'risk_level': risk_level,
                'verdict': verdict
            }
            
            return is_fraud, confidence, result
            
        except Exception as e:
            print(f"Error in fraud prediction: {str(e)}")
            return None, 0, {}
    
    def predict_quality_tier(self, features_dict):
        """Predict resume quality tier"""
        if not self.models_loaded:
            return None, 0
        
        try:
            X = pd.DataFrame([features_dict])[self.feature_columns]
            
            quality_encoded = self.quality_tier_model.predict(X)[0]
            quality = self.quality_encoder.inverse_transform([quality_encoded])[0]
            
            if hasattr(self.quality_tier_model, 'predict_proba'):
                proba = self.quality_tier_model.predict_proba(X)[0]
                confidence = int(max(proba) * 100)
            else:
                confidence = 90
            
            return quality, confidence
            
        except Exception as e:
            print(f"Error in quality prediction: {str(e)}")
            return None, 0
    
    def get_all_predictions(self, resume_data, resume_text):
        """
        Get all ML predictions at once
        
        Returns:
            Dictionary with all predictions
        """
        # Extract features
        features = self.extract_ml_features(resume_data, resume_text)
        
        # Get all predictions
        predictions = {
            'features': features,
            'ml_enabled': self.models_loaded
        }
        
        if self.models_loaded:
            # ATS Score
            ats_score, ats_conf = self.predict_ats_score(features)
            predictions['ats_score'] = ats_score
            predictions['ats_confidence'] = ats_conf
            
            # Job Role
            job_role, role_conf = self.predict_job_role(features)
            predictions['job_role'] = job_role
            predictions['role_confidence'] = role_conf
            
            # Experience Level
            exp_level, exp_conf = self.predict_experience_level(features)
            predictions['experience_level'] = exp_level
            predictions['experience_confidence'] = exp_conf
            
            # Fraud Detection
            is_fraud, fraud_conf, fraud_result = self.predict_fraud(features)
            predictions['fraud_detection'] = fraud_result
            
            # Quality Tier
            quality, quality_conf = self.predict_quality_tier(features)
            predictions['quality_tier'] = quality
            predictions['quality_confidence'] = quality_conf
        
        return predictions


# Global predictor instance
_predictor = None

def get_predictor():
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = ResumeMLPredictor()
    return _predictor


if __name__ == "__main__":
    # Test the predictor
    print("Testing ML Predictor...")
    predictor = ResumeMLPredictor()
    
    # Create dummy resume data for testing
    test_resume_data = {
        'skills': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'NumPy'],
        'experience_years': 3,
        'no_of_pages': 2
    }
    
    test_resume_text = """
    John Doe
    Data Scientist
    
    Summary: Experienced data scientist with 3 years of experience in machine learning.
    
    Skills: Python, Machine Learning, TensorFlow, PyTorch, Pandas, NumPy
    
    Experience:
    Data Scientist at TechCorp (2021-2024)
    - Built ML models that improved accuracy by 25%
    - Managed 5 projects with over 1000 users
    - Developed automated pipelines
    
    Projects:
    - Predictive Analytics Tool
    - Customer Segmentation System
    
    Education:
    B.Tech in Computer Science, 2021
    
    LinkedIn: linkedin.com/in/johndoe
    GitHub: github.com/johndoe
    """
    
    predictions = predictor.get_all_predictions(test_resume_data, test_resume_text)
    
    print("\n📊 Predictions:")
    print(f"   ATS Score: {predictions.get('ats_score')} ({predictions.get('ats_confidence')}% confidence)")
    print(f"   Job Role: {predictions.get('job_role')} ({predictions.get('role_confidence')}% confidence)")
    print(f"   Experience Level: {predictions.get('experience_level')}")
    print(f"   Quality: {predictions.get('quality_tier')}")
    print(f"   Fraud Detection: {predictions.get('fraud_detection', {}).get('verdict')}")
