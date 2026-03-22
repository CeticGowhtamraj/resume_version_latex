"""
Training Data Generator for Resume Analyzer ML Models
Generates realistic synthetic resume data for training
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# ==================== CONFIGURATION ====================

ROLES = [
    'Data Scientist', 'Data Analyst', 'Data Engineer',
    'Software Engineer', 'Web Developer', 'Mobile Developer',
    'UI/UX Designer', 'DevOps Engineer'
]

EXPERIENCE_LEVELS = ['Fresher', 'Entry Level', 'Intermediate', 'Senior', 'Expert']

QUALITY_TIERS = ['Excellent', 'Good', 'Fair', 'Poor']

# ==================== REALISTIC DISTRIBUTIONS ====================

def generate_name():
    """Generate random names"""
    first_names = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Rohan', 'Anjali', 'Vikram', 'Divya',
                   'Arjun', 'Pooja', 'Karthik', 'Meera', 'Aditya', 'Neha', 'Sanjay', 'Riya']
    last_names = ['Sharma', 'Kumar', 'Singh', 'Patel', 'Gupta', 'Mehta', 'Shah', 'Reddy',
                  'Nair', 'Iyer', 'Joshi', 'Kapoor', 'Desai', 'Rao', 'Kulkarni']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_email(name):
    """Generate email from name"""
    name_part = name.lower().replace(' ', '.')
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
    return f"{name_part}{random.randint(1, 99)}@{random.choice(domains)}"

def generate_phone():
    """Generate Indian phone number"""
    return f"+91-{random.randint(70000, 99999)}-{random.randint(10000, 99999)}"

# ==================== FEATURE GENERATION ====================

def generate_resume_features(role, experience_level, quality_tier, is_fraud=False):
    """
    Generate realistic resume features based on role, experience, and quality
    """
    
    # Experience years mapping
    exp_mapping = {
        'Fresher': (0, 0),
        'Entry Level': (1, 2),
        'Intermediate': (3, 5),
        'Senior': (6, 10),
        'Expert': (11, 20)
    }
    exp_min, exp_max = exp_mapping[experience_level]
    experience_years = random.randint(exp_min, exp_max) if exp_max > exp_min else 0
    
    # Skills count based on experience and quality
    base_skills = {
        'Fresher': (5, 12),
        'Entry Level': (8, 15),
        'Intermediate': (12, 20),
        'Senior': (15, 25),
        'Expert': (18, 30)
    }
    
    quality_multiplier = {
        'Excellent': 1.0,
        'Good': 0.85,
        'Fair': 0.7,
        'Poor': 0.5
    }
    
    min_skills, max_skills = base_skills[experience_level]
    multiplier = quality_multiplier[quality_tier]
    
    if is_fraud:
        # Fraudulent resumes often have too many skills for experience
        skills_count = int(random.randint(max_skills + 10, max_skills + 30))
    else:
        skills_count = int(random.randint(int(min_skills * multiplier), int(max_skills * multiplier)))
    
    # Professional links
    has_linkedin = random.random() < (0.95 if quality_tier in ['Excellent', 'Good'] else 0.6)
    has_github = random.random() < (0.85 if role in ['Data Scientist', 'Software Engineer', 'Data Engineer'] 
                                    and quality_tier in ['Excellent', 'Good'] else 0.4)
    has_portfolio = random.random() < (0.7 if role in ['UI/UX Designer', 'Web Developer'] 
                                       and quality_tier in ['Excellent', 'Good'] else 0.3)
    
    # Professional summary
    has_summary = random.random() < (0.95 if quality_tier == 'Excellent' else 
                                    0.8 if quality_tier == 'Good' else 
                                    0.6 if quality_tier == 'Fair' else 0.3)
    
    summary_length = 0
    if has_summary:
        summary_length = random.randint(100, 250) if quality_tier == 'Excellent' else \
                        random.randint(60, 150) if quality_tier == 'Good' else \
                        random.randint(30, 100)
    
    # Projects
    project_base = {
        'Fresher': (1, 3),
        'Entry Level': (2, 4),
        'Intermediate': (3, 6),
        'Senior': (4, 8),
        'Expert': (5, 10)
    }
    min_proj, max_proj = project_base[experience_level]
    project_count = random.randint(int(min_proj * multiplier), int(max_proj * multiplier))
    
    if is_fraud:
        # Fraudulent resumes claim many projects without details
        project_count = random.randint(max_proj + 5, max_proj + 15)
    
    # Education
    has_education = random.random() < (0.98 if quality_tier in ['Excellent', 'Good'] else 0.85)
    education_score = random.randint(8, 10) if quality_tier == 'Excellent' else \
                     random.randint(6, 9) if quality_tier == 'Good' else \
                     random.randint(4, 7) if quality_tier == 'Fair' else \
                     random.randint(2, 5)
    
    # Page count
    page_count = 1 if experience_years <= 3 else \
                2 if experience_years <= 8 else \
                random.choice([2, 3])
    
    if quality_tier == 'Poor':
        page_count = random.choice([1, 3, 4])  # Either too short or too long
    
    # Action verbs (strong indicator of quality)
    action_verbs_count = random.randint(10, 20) if quality_tier == 'Excellent' else \
                        random.randint(6, 12) if quality_tier == 'Good' else \
                        random.randint(3, 8) if quality_tier == 'Fair' else \
                        random.randint(0, 4)
    
    # Quantifiable metrics (numbers, percentages)
    metrics_count = random.randint(5, 12) if quality_tier == 'Excellent' else \
                   random.randint(3, 7) if quality_tier == 'Good' else \
                   random.randint(1, 4) if quality_tier == 'Fair' else \
                   random.randint(0, 2)
    
    if is_fraud:
        # Fraudulent resumes often lack concrete metrics
        metrics_count = max(0, metrics_count - random.randint(3, 6))
    
    # Role-specific keywords
    role_keyword_base = {
        'Data Scientist': 15,
        'Data Analyst': 12,
        'Data Engineer': 13,
        'Software Engineer': 14,
        'Web Developer': 11,
        'Mobile Developer': 10,
        'UI/UX Designer': 9,
        'DevOps Engineer': 12
    }
    
    base_keywords = role_keyword_base.get(role, 10)
    role_keywords_count = int(base_keywords * multiplier)
    
    if is_fraud:
        # Fraudulent resumes may have inflated keywords
        role_keywords_count += random.randint(5, 15)
    
    # Work experience sections with dates
    has_work_experience = experience_years > 0 or random.random() < 0.3  # Some freshers have internships
    work_experience_dates_count = 0
    
    if has_work_experience:
        if experience_years == 0:
            work_experience_dates_count = random.randint(1, 2)  # Internships
        elif experience_years <= 2:
            work_experience_dates_count = random.randint(1, 2)
        elif experience_years <= 5:
            work_experience_dates_count = random.randint(2, 3)
        else:
            work_experience_dates_count = random.randint(2, 5)
    
    if is_fraud:
        # Fraudulent resumes may lack proper dates
        work_experience_dates_count = max(0, work_experience_dates_count - random.randint(1, 3))
    
    # Certifications
    cert_count = random.randint(2, 5) if quality_tier == 'Excellent' and experience_years >= 2 else \
                random.randint(1, 3) if quality_tier == 'Good' else \
                random.randint(0, 2)
    
    # Skills-to-projects ratio (important fraud indicator)
    if project_count > 0:
        skills_per_project = skills_count / project_count
    else:
        skills_per_project = skills_count  # Red flag
    
    # Context validation score (0-100)
    if is_fraud:
        context_validation_score = random.randint(10, 40)
    else:
        context_validation_score = random.randint(60, 100) if quality_tier == 'Excellent' else \
                                  random.randint(45, 75) if quality_tier == 'Good' else \
                                  random.randint(30, 60) if quality_tier == 'Fair' else \
                                  random.randint(15, 45)
    
    # Achievement indicators
    has_achievements = random.random() < (0.9 if quality_tier == 'Excellent' else 
                                         0.7 if quality_tier == 'Good' else 0.4)
    
    return {
        'skills_count': skills_count,
        'experience_years': experience_years,
        'has_linkedin': int(has_linkedin),
        'has_github': int(has_github),
        'has_portfolio': int(has_portfolio),
        'has_summary': int(has_summary),
        'summary_length': summary_length,
        'project_count': project_count,
        'has_education': int(has_education),
        'education_score': education_score,
        'page_count': page_count,
        'action_verbs_count': action_verbs_count,
        'metrics_count': metrics_count,
        'role_keywords_count': role_keywords_count,
        'work_experience_dates_count': work_experience_dates_count,
        'certification_count': cert_count,
        'skills_per_project': round(skills_per_project, 2),
        'context_validation_score': context_validation_score,
        'has_achievements': int(has_achievements),
    }

# ==================== ATS SCORE CALCULATION ====================

def calculate_realistic_ats_score(features, quality_tier, is_fraud):
    """
    Calculate realistic ATS score based on features
    This mimics the scoring logic in the main app
    """
    score = 0
    
    # Contact info (18 points)
    score += 7  # Email (always present in training data)
    score += 6  # Phone (always present)
    
    if features['has_linkedin'] and features['has_github']:
        score += 5
    elif features['has_linkedin'] or features['has_github']:
        score += 3
    else:
        score += 1
    
    # Professional summary (8 points)
    if features['has_summary']:
        if features['summary_length'] >= 100:
            score += 8
        elif features['summary_length'] >= 50:
            score += 5
        else:
            score += 3
    else:
        score += 1
    
    # Skills (22 points)
    if features['skills_count'] >= 18:
        score += 22
    elif features['skills_count'] >= 12:
        score += 18
    elif features['skills_count'] >= 8:
        score += 14
    elif features['skills_count'] >= 5:
        score += 9
    else:
        score += 4
    
    # Experience (25 points)
    if features['work_experience_dates_count'] >= 4:
        score += 25
    elif features['work_experience_dates_count'] >= 2:
        score += 20
    elif features['work_experience_dates_count'] >= 1:
        score += 15
    else:
        if features['experience_years'] > 0:
            score += 10
        else:
            score += 5
    
    # Education (10 points)
    if features['has_education']:
        score += features['education_score']
    else:
        score += 2
    
    # Projects (12 points)
    if features['project_count'] >= 3:
        score += 12
    elif features['project_count'] >= 2:
        score += 9
    elif features['project_count'] >= 1:
        score += 5
    else:
        score += 2
    
    # Quality adjustments
    if features['action_verbs_count'] >= 8:
        score += 3
    elif features['action_verbs_count'] >= 4:
        score += 1
    
    if features['metrics_count'] >= 4:
        score += 2
    
    # Fraud penalty
    if is_fraud:
        score -= random.randint(15, 35)
    
    # Page count adjustment
    if features['page_count'] in [1, 2]:
        score += 2
    elif features['page_count'] >= 4:
        score -= 5
    
    return max(0, min(100, score))

# ==================== MAIN GENERATION ====================

def generate_training_dataset(num_samples=2000, fraud_ratio=0.15):
    """
    Generate comprehensive training dataset
    
    Args:
        num_samples: Total number of samples to generate
        fraud_ratio: Proportion of fraudulent resumes (default 15%)
    """
    
    print(f"🎯 Generating {num_samples} training samples...")
    print(f"   Fraud samples: {int(num_samples * fraud_ratio)}")
    print(f"   Legitimate samples: {int(num_samples * (1 - fraud_ratio))}")
    
    data = []
    
    # Distribution of samples across categories
    # Quality distribution: Excellent 25%, Good 35%, Fair 25%, Poor 15%
    quality_distribution = {
        'Excellent': 0.25,
        'Good': 0.35,
        'Fair': 0.25,
        'Poor': 0.15
    }
    
    # Experience distribution: Fresher 20%, Entry 25%, Intermediate 30%, Senior 20%, Expert 5%
    exp_distribution = {
        'Fresher': 0.20,
        'Entry Level': 0.25,
        'Intermediate': 0.30,
        'Senior': 0.20,
        'Expert': 0.05
    }
    
    fraud_count = int(num_samples * fraud_ratio)
    legitimate_count = num_samples - fraud_count
    
    # Generate legitimate samples
    for i in range(legitimate_count):
        role = random.choice(ROLES)
        
        # Select experience level based on distribution
        exp_level = np.random.choice(
            list(exp_distribution.keys()),
            p=list(exp_distribution.values())
        )
        
        # Select quality tier based on distribution
        quality = np.random.choice(
            list(quality_distribution.keys()),
            p=list(quality_distribution.values())
        )
        
        name = generate_name()
        email = generate_email(name)
        phone = generate_phone()
        
        features = generate_resume_features(role, exp_level, quality, is_fraud=False)
        ats_score = calculate_realistic_ats_score(features, quality, is_fraud=False)
        
        # Add some realistic noise to scores
        ats_score += random.randint(-3, 3)
        ats_score = max(0, min(100, ats_score))
        
        sample = {
            'resume_id': f'RES_{i+1:05d}',
            'name': name,
            'email': email,
            'phone': phone,
            **features,
            'ats_score': ats_score,
            'job_role': role,
            'experience_level': exp_level,
            'quality_tier': quality,
            'is_fraud': 0
        }
        
        data.append(sample)
        
        if (i + 1) % 500 == 0:
            print(f"   Generated {i+1} legitimate samples...")
    
    # Generate fraudulent samples
    for i in range(fraud_count):
        # Frauds are more common in certain categories
        role = random.choice(ROLES)
        
        # Frauds often claim higher experience
        exp_level = np.random.choice(
            ['Entry Level', 'Intermediate', 'Senior', 'Expert'],
            p=[0.15, 0.35, 0.35, 0.15]
        )
        
        # Frauds can appear in any quality tier but often Poor/Fair
        quality = np.random.choice(
            ['Poor', 'Fair', 'Good', 'Excellent'],
            p=[0.4, 0.35, 0.20, 0.05]
        )
        
        name = generate_name()
        email = generate_email(name)
        phone = generate_phone()
        
        features = generate_resume_features(role, exp_level, quality, is_fraud=True)
        ats_score = calculate_realistic_ats_score(features, quality, is_fraud=True)
        
        # Fraud scores tend to be lower
        ats_score += random.randint(-5, 0)
        ats_score = max(0, min(100, ats_score))
        
        sample = {
            'resume_id': f'RES_{legitimate_count + i+1:05d}',
            'name': name,
            'email': email,
            'phone': phone,
            **features,
            'ats_score': ats_score,
            'job_role': role,
            'experience_level': exp_level,
            'quality_tier': quality,
            'is_fraud': 1
        }
        
        data.append(sample)
        
        if (i + 1) % 200 == 0:
            print(f"   Generated {i+1} fraud samples...")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the data
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"\n✅ Dataset generation complete!")
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(df)}")
    print(f"   Legitimate: {len(df[df['is_fraud'] == 0])}")
    print(f"   Fraudulent: {len(df[df['is_fraud'] == 1])}")
    print(f"\n   Role distribution:")
    print(df['job_role'].value_counts())
    print(f"\n   Experience distribution:")
    print(df['experience_level'].value_counts())
    print(f"\n   Quality distribution:")
    print(df['quality_tier'].value_counts())
    print(f"\n   ATS Score statistics:")
    print(df['ats_score'].describe())
    
    return df

# ==================== SAVE DATASETS ====================

if __name__ == "__main__":
    print("=" * 70)
    print("📚 RESUME ANALYZER - TRAINING DATA GENERATOR")
    print("=" * 70)
    print()
    
    # Generate main training dataset
    df_train = generate_training_dataset(num_samples=2000, fraud_ratio=0.15)
    
    # Save to CSV
    train_file = 'resume_training_data.csv'
    df_train.to_csv(train_file, index=False)
    print(f"\n💾 Training data saved to: {train_file}")
    
    # Generate smaller test dataset
    print(f"\n{'='*70}")
    print("Generating test dataset...")
    print("=" * 70)
    print()
    df_test = generate_training_dataset(num_samples=500, fraud_ratio=0.15)
    
    test_file = 'resume_test_data.csv'
    df_test.to_csv(test_file, index=False)
    print(f"\n💾 Test data saved to: {test_file}")
    
    print(f"\n{'='*70}")
    print("✅ ALL DATASETS GENERATED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"\n📁 Files created:")
    print(f"   1. {train_file} (2000 samples)")
    print(f"   2. {test_file} (500 samples)")
    print(f"\n🚀 Next step: Run 'python train_models.py' to train ML models")