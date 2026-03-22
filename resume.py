"""
Enhanced AI Resume Analyzer with Comprehensive UI
Features:
- ATS Score, Overall Score, Authentication Score
- Personal Details Extraction
- Experience Details
- Advantages & Disadvantages (Categorized)
- Personalized Suggestions
"""

import streamlit as st
import PyPDF2
import docx
import re
from datetime import datetime
from ml_predictor import get_predictor
from improved_analyzer_fixed import ImprovedResumeAnalyzer
import json

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main Theme */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Score Cards */
    .score-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid;
        transition: transform 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .score-card.excellent {
        border-left-color: #10b981;
    }
    
    .score-card.good {
        border-left-color: #3b82f6;
    }
    
    .score-card.average {
        border-left-color: #f59e0b;
    }
    
    .score-card.poor {
        border-left-color: #ef4444;
    }
    
    .score-number {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-label {
        font-size: 1rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Info Cards */
    .info-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .info-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    
    .info-value {
        font-size: 1.1rem;
        color: #1e293b;
        font-weight: 600;
    }
    
    /* Advantage/Disadvantage Cards */
    .adv-card {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .dis-card {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Suggestion Cards */
    .suggestion-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .suggestion-card strong {
        color: #92400e;
    }
    
    /* Badge Styles */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.3rem;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background: #fed7aa;
        color: #92400e;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    /* Progress Bar */
    .progress-bar {
        background: #e5e7eb;
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        transition: width 1s ease;
    }
    
    /* Experience Timeline */
    .timeline-item {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .timeline-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .timeline-date {
        font-size: 0.9rem;
        color: #64748b;
        font-style: italic;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


class ResumeAnalyzer:
    """Enhanced Resume Analyzer with comprehensive extraction and analysis"""
    
    def __init__(self):
        """Initialize the analyzer with ML predictor"""
        self.predictor = get_predictor()
    
    def extract_text_from_file(self, uploaded_file):
        """Extract text from PDF or DOCX file"""
        text = ""
        
        try:
            if uploaded_file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                    
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                for para in doc.paragraphs:
                    text += para.text + "\n"
                    
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            
        return text.strip()
    
    def extract_personal_details(self, text):
        """Extract personal information from resume"""
        details = {
            'name': None,
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None,
            'location': None,
            'portfolio': None
        }
        
        # Extract Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            details['email'] = email_match.group()
        
        # Extract Phone (various formats)
        phone_patterns = [
            r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',  # US format
            r'\+?(\d{1,3})[\s.-]?(\d{3,4})[\s.-]?(\d{3,4})[\s.-]?(\d{3,4})',  # International
            r'\b\d{10}\b'  # Simple 10-digit
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                details['phone'] = phone_match.group()
                break
        
        # Extract Name (first few words before email/phone or from first line)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) < 50:
                if not re.search(r'resume|curriculum|vitae|cv', line, re.IGNORECASE):
                    details['name'] = line
                    break
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            details['linkedin'] = linkedin_match.group()
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            details['github'] = github_match.group()
        
        # Extract Portfolio/Website
        portfolio_patterns = [
            r'portfolio:\s*(https?://\S+)',
            r'website:\s*(https?://\S+)',
            r'(https?://(?:www\.)?[\w-]+\.(?:com|io|dev|net)/?)'
        ]
        for pattern in portfolio_patterns:
            portfolio_match = re.search(pattern, text, re.IGNORECASE)
            if portfolio_match:
                url = portfolio_match.group(1) if portfolio_match.lastindex else portfolio_match.group()
                if 'linkedin' not in url.lower() and 'github' not in url.lower():
                    details['portfolio'] = url
                    break
        
        # Extract Location
        location_pattern = r'(?:location|address|city):\s*([^,\n]+(?:,\s*[^,\n]+)*)'
        location_match = re.search(location_pattern, text, re.IGNORECASE)
        if location_match:
            details['location'] = location_match.group(1).strip()
        
        return details
    
    def extract_skills(self, text):
        """Extract technical and soft skills from resume"""
        # Common technical skills database
        technical_skills = {
            'Programming Languages': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 
                                     'php', 'swift', 'kotlin', 'typescript', 'r', 'matlab', 'scala'],
            'Web Technologies': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 
                               'django', 'flask', 'spring', 'asp.net', 'jquery', 'bootstrap'],
            'Databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis', 'cassandra', 
                         'dynamodb', 'sqlite', 'mariadb'],
            'Cloud & DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 
                             'ansible', 'ci/cd', 'git', 'github', 'gitlab'],
            'Data Science & ML': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 
                                 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'nlp', 'computer vision'],
            'Tools & Frameworks': ['excel', 'tableau', 'power bi', 'jira', 'confluence', 'postman', 
                                  'vscode', 'intellij', 'eclipse'],
            'Mobile Development': ['android', 'ios', 'react native', 'flutter', 'xamarin'],
            'Other': ['agile', 'scrum', 'api', 'rest', 'graphql', 'microservices', 'testing', 'selenium']
        }
        
        soft_skills = ['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical', 
                      'creative', 'adaptability', 'time management', 'critical thinking', 'collaboration']
        
        text_lower = text.lower()
        
        found_skills = {'technical': {}, 'soft': []}
        
        # Find technical skills by category
        for category, skills_list in technical_skills.items():
            found_in_category = []
            for skill in skills_list:
                if skill in text_lower:
                    found_in_category.append(skill.title())
            if found_in_category:
                found_skills['technical'][category] = found_in_category
        
        # Find soft skills
        for skill in soft_skills:
            if skill in text_lower:
                found_skills['soft'].append(skill.title())
        
        return found_skills
    
    def extract_experience(self, text):
        """Extract work experience details"""
        experiences = []
        
        # Look for experience section
        exp_section_pattern = r'(?:experience|employment|work history)[\s:]*\n(.*?)(?=\n(?:education|skills|projects|certifications)|$)'
        exp_match = re.search(exp_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if exp_match:
            exp_text = exp_match.group(1)
            
            # Extract individual experiences
            # Pattern for job entries (company, role, dates)
            job_patterns = [
                r'([^\n]+)\s+(?:at|@)\s+([^\n]+)\s+\(?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}).*?(?:Present|Current|\d{4}))\)?',
                r'([^\n]+)\s*\n\s*([^\n]+)\s*\n\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}).*?(?:Present|Current|\d{4}))'
            ]
            
            for pattern in job_patterns:
                matches = re.findall(pattern, exp_text, re.IGNORECASE)
                for match in matches:
                    experiences.append({
                        'role': match[0].strip(),
                        'company': match[1].strip(),
                        'duration': match[2].strip(),
                        'description': ''
                    })
        
        # Calculate total years of experience
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience'
        years_match = re.search(years_pattern, text, re.IGNORECASE)
        total_years = int(years_match.group(1)) if years_match else len(experiences)
        
        return {
            'experiences': experiences,
            'total_years': total_years,
            'total_positions': len(experiences)
        }
    
    def extract_education(self, text):
        """Extract education details"""
        education = []
        
        # Common degrees
        degree_patterns = [
            r'((?:Bachelor|Master|PhD|Ph\.D|B\.Tech|M\.Tech|B\.S|M\.S|MBA).*?)(?:\n|,|\d{4})',
            r'((?:B\.E|M\.E|B\.A|M\.A).*?)(?:\n|,|\d{4})'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match not in education:
                    education.append(match.strip())
        
        # Extract universities
        university_pattern = r'(?:university|college|institute)\s+of\s+[\w\s]+'
        universities = re.findall(university_pattern, text, re.IGNORECASE)
        
        return {
            'degrees': education,
            'universities': universities
        }
    
    def extract_projects(self, text):
        """Extract project details"""
        projects = []
        
        # Look for project section
        project_pattern = r'(?:projects?|portfolio)[\s:]*\n(.*?)(?=\n(?:experience|education|skills|certifications)|$)'
        project_match = re.search(project_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if project_match:
            project_text = project_match.group(1)
            
            # Split by bullet points or numbers
            project_items = re.split(r'\n\s*[-•●]\s*|\n\s*\d+\.\s*', project_text)
            
            for item in project_items:
                item = item.strip()
                if len(item) > 20:  # Filter out noise
                    projects.append(item)
        
        return projects[:5]  # Return top 5 projects
    
    def calculate_overall_score(self, ml_predictions, extracted_data):
        """Calculate comprehensive overall score"""
        scores = {
            'ats_score': ml_predictions.get('ats_score', 0) or 0,
            'completeness': 0,
            'experience': 0,
            'skills': 0,
            'formatting': 0
        }
        
        # Completeness Score (25%)
        personal_details = extracted_data.get('personal_details', {})
        completeness_factors = [
            personal_details.get('email') is not None,
            personal_details.get('phone') is not None,
            personal_details.get('linkedin') is not None,
            extracted_data.get('experience', {}).get('total_positions', 0) > 0,
            len(extracted_data.get('skills', {}).get('technical', {})) > 0
        ]
        scores['completeness'] = (sum(completeness_factors) / len(completeness_factors)) * 25
        
        # Experience Score (25%)
        exp_years = extracted_data.get('experience', {}).get('total_years', 0)
        scores['experience'] = min(exp_years * 5, 25)
        
        # Skills Score (25%)
        total_skills = sum(len(skills) for skills in extracted_data.get('skills', {}).get('technical', {}).values())
        scores['skills'] = min(total_skills * 2, 25)
        
        # Formatting Score (25%)
        features = ml_predictions.get('features', {})
        formatting_factors = [
            features.get('has_summary', 0),
            features.get('action_verbs_count', 0) > 5,
            features.get('metrics_count', 0) > 0,
            features.get('page_count', 0) <= 2
        ]
        scores['formatting'] = (sum(formatting_factors) / len(formatting_factors)) * 25
        
        overall_score = sum(scores.values())
        
        return overall_score, scores
    
    def analyze_advantages_disadvantages(self, ml_predictions, extracted_data):
        """Categorize advantages and disadvantages"""
        features = ml_predictions.get('features', {})
        skills_data = extracted_data.get('skills', {})
        
        advantages = {
            'Skills': [],
            'Experience': [],
            'Content': [],
            'Formatting': [],
            'Profile': []
        }
        
        disadvantages = {
            'Skills': [],
            'Experience': [],
            'Content': [],
            'Formatting': [],
            'Profile': []
        }
        
        # Skills Analysis
        total_skills = sum(len(s) for s in skills_data.get('technical', {}).values())
        if total_skills >= 10:
            advantages['Skills'].append(f"Strong technical skill set with {total_skills} skills listed")
        elif total_skills < 5:
            disadvantages['Skills'].append(f"Limited technical skills ({total_skills} found) - add more relevant skills")
        
        if skills_data.get('soft', []):
            advantages['Skills'].append(f"Soft skills mentioned: {', '.join(skills_data['soft'][:3])}")
        else:
            disadvantages['Skills'].append("No soft skills mentioned - add leadership, communication, etc.")
        
        # Experience Analysis
        exp_years = extracted_data.get('experience', {}).get('total_years', 0)
        exp_positions = extracted_data.get('experience', {}).get('total_positions', 0)
        
        if exp_years >= 3:
            advantages['Experience'].append(f"{exp_years}+ years of professional experience")
        elif exp_years < 1:
            disadvantages['Experience'].append("Limited work experience - highlight internships or projects")
        
        if exp_positions >= 2:
            advantages['Experience'].append(f"Diverse experience across {exp_positions} positions")
        elif exp_positions == 0:
            disadvantages['Experience'].append("No work experience section found")
        
        # Content Analysis
        if features.get('metrics_count', 0) >= 3:
            advantages['Content'].append(f"{features['metrics_count']} quantifiable achievements mentioned")
        else:
            disadvantages['Content'].append("Lack of quantifiable achievements - add numbers, percentages, metrics")
        
        if features.get('action_verbs_count', 0) >= 5:
            advantages['Content'].append(f"Strong action verbs used ({features['action_verbs_count']} instances)")
        else:
            disadvantages['Content'].append("Use more action verbs (Led, Developed, Achieved, etc.)")
        
        if features.get('project_count', 0) >= 2:
            advantages['Content'].append(f"{features['project_count']} projects showcased")
        else:
            disadvantages['Content'].append("Add more project details to demonstrate practical experience")
        
        # Formatting Analysis
        if features.get('has_summary', 0):
            advantages['Formatting'].append("Professional summary/objective present")
        else:
            disadvantages['Formatting'].append("Missing professional summary - add a compelling intro")
        
        page_count = features.get('page_count', 1)
        if page_count <= 2:
            advantages['Formatting'].append(f"Concise format ({page_count} page{'s' if page_count > 1 else ''})")
        else:
            disadvantages['Formatting'].append(f"Resume too long ({page_count} pages) - keep it under 2 pages")
        
        # Profile Analysis
        if features.get('has_linkedin', 0):
            advantages['Profile'].append("LinkedIn profile included")
        else:
            disadvantages['Profile'].append("Add LinkedIn profile URL")
        
        if features.get('has_github', 0):
            advantages['Profile'].append("GitHub profile included")
        elif 'Programming' in skills_data.get('technical', {}):
            disadvantages['Profile'].append("Add GitHub profile to showcase code samples")
        
        if features.get('has_portfolio', 0):
            advantages['Profile'].append("Portfolio/website included")
        
        # Remove empty categories
        advantages = {k: v for k, v in advantages.items() if v}
        disadvantages = {k: v for k, v in disadvantages.items() if v}
        
        return advantages, disadvantages
    
    def generate_personalized_suggestions(self, ml_predictions, extracted_data, disadvantages):
        """Generate actionable suggestions for resume improvement"""
        suggestions = []
        features = ml_predictions.get('features', {})
        ats_score = ml_predictions.get('ats_score', 0)
        
        # Priority suggestions based on ATS score
        if ats_score < 60:
            suggestions.append({
                'priority': 'High',
                'category': 'Overall Structure',
                'suggestion': 'Complete resume overhaul recommended. Focus on adding quantifiable achievements, relevant keywords, and proper formatting.',
                'impact': '+20-30 points'
            })
        
        # Skills suggestions
        if features.get('skills_count', 0) < 8:
            suggestions.append({
                'priority': 'High',
                'category': 'Technical Skills',
                'suggestion': 'Add more relevant technical skills (target: 10-15 skills). Include both core competencies and supporting technologies.',
                'impact': '+5-10 points'
            })
        
        # Metrics suggestions
        if features.get('metrics_count', 0) < 3:
            suggestions.append({
                'priority': 'High',
                'category': 'Achievements',
                'suggestion': 'Quantify your achievements with numbers. Examples: "Increased efficiency by 30%", "Managed team of 5", "Reduced costs by $50K".',
                'impact': '+10-15 points'
            })
        
        # Action verbs
        if features.get('action_verbs_count', 0) < 5:
            suggestions.append({
                'priority': 'Medium',
                'category': 'Content Quality',
                'suggestion': 'Use strong action verbs to start bullet points: Developed, Led, Implemented, Optimized, Achieved, Designed.',
                'impact': '+5-8 points'
            })
        
        # Professional summary
        if not features.get('has_summary', 0):
            suggestions.append({
                'priority': 'Medium',
                'category': 'Professional Summary',
                'suggestion': 'Add a compelling 3-4 line professional summary at the top highlighting your expertise and career goals.',
                'impact': '+5-7 points'
            })
        
        # Projects
        if features.get('project_count', 0) < 2:
            suggestions.append({
                'priority': 'High',
                'category': 'Projects',
                'suggestion': 'Add 2-4 detailed projects showcasing your skills. Include technologies used, your role, and measurable outcomes.',
                'impact': '+8-12 points'
            })
        
        # LinkedIn
        if not features.get('has_linkedin', 0):
            suggestions.append({
                'priority': 'Low',
                'category': 'Professional Presence',
                'suggestion': 'Add your LinkedIn profile URL. Ensure your LinkedIn is complete and matches your resume.',
                'impact': '+3-5 points'
            })
        
        # GitHub (for technical roles)
        job_role = ml_predictions.get('job_role', '').lower()
        if 'developer' in job_role or 'engineer' in job_role or 'scientist' in job_role:
            if not features.get('has_github', 0):
                suggestions.append({
                    'priority': 'Medium',
                    'category': 'Portfolio',
                    'suggestion': 'Add GitHub profile with 3-5 projects. Active GitHub presence is crucial for technical roles.',
                    'impact': '+5-8 points'
                })
        
        # Page length
        if features.get('page_count', 1) > 2:
            suggestions.append({
                'priority': 'Medium',
                'category': 'Formatting',
                'suggestion': 'Reduce resume to 1-2 pages. Focus on most relevant and recent experiences. Use concise bullet points.',
                'impact': '+3-5 points'
            })
        
        # Education
        if features.get('education_score', 0) < 7:
            suggestions.append({
                'priority': 'Low',
                'category': 'Education',
                'suggestion': 'Ensure education section includes degree, institution, graduation year, and relevant coursework or GPA if strong (>3.5).',
                'impact': '+2-4 points'
            })
        
        # Context validation
        if features.get('context_validation_score', 0) < 50:
            suggestions.append({
                'priority': 'High',
                'category': 'Content Depth',
                'suggestion': 'Provide more context for your skills. Don\'t just list technologies - show how you used them in real projects.',
                'impact': '+10-15 points'
            })
        
        # Sort by priority
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        suggestions.sort(key=lambda x: priority_order[x['priority']])
        
        return suggestions


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
        <div class='main-header'>
            <h1>🤖 AI Resume Analyzer Pro</h1>
            <p>Get comprehensive insights, AI-powered scoring, and personalized recommendations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = ImprovedResumeAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 About This Tool")
        st.info("""
        This AI-powered tool provides:
        - **ATS Score** (0-100)
        - **Overall Resume Score**
        - **Authenticity Analysis**
        - **Detailed Insights**
        - **Personalized Suggestions**
        """)
        
        st.markdown("### 🎯 Scoring Guide")
        st.markdown("""
        - **90-100**: Excellent 🌟
        - **75-89**: Good ✅
        - **60-74**: Average ⚠️
        - **Below 60**: Needs Work ❌
        """)
        
        if analyzer.predictor.models_loaded:
            st.success("✅ ML Models Active")
        else:
            st.warning("⚠️ Rule-based Mode")
    
    # File Upload
    st.markdown("### 📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF or DOCX format)",
        type=["pdf", "docx"],
        help="Upload a PDF or Word document of your resume"
    )
    
    if uploaded_file is not None:
        # Extract text
        with st.spinner("📖 Reading your resume..."):
            resume_text = analyzer.extract_text_from_file(uploaded_file)
        
        if not resume_text or len(resume_text) < 100:
            st.error("❌ Unable to extract sufficient text from the resume. Please check the file and try again.")
            return
        
        # Show preview
        with st.expander("📄 Resume Text Preview"):
            st.text_area("Extracted Text", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200)
        
        # Extract all data
        with st.spinner("🔍 Analyzing resume..."):
            personal_details = analyzer.extract_personal_details(resume_text)
            skills_data = analyzer.extract_skills(resume_text)
            experience_data = analyzer.extract_experience(resume_text)
            education_data = analyzer.extract_education(resume_text)
            projects = analyzer.extract_projects(resume_text)
            
            # Prepare data for ML
            resume_data = {
                'skills': [skill for category in skills_data.get('technical', {}).values() for skill in category],
                'experience_years': experience_data.get('total_years', 0),
                'no_of_pages': resume_text.count('\f') + 1  # Approximate page count
            }
            
            # Get ML predictions
            ml_predictions = analyzer.predictor.get_all_predictions(resume_data, resume_text)
            
            # Extract all data
            extracted_data = {
                'personal_details': personal_details,
                'skills': skills_data,
                'experience': experience_data,
                'education': education_data,
                'projects': projects
            }
            
            # Calculate overall score
            overall_score, score_breakdown = analyzer.calculate_overall_score(ml_predictions, extracted_data)
            
            # Analyze advantages and disadvantages
            advantages, disadvantages = analyzer.analyze_advantages_disadvantages(ml_predictions, extracted_data)
            
            # Generate suggestions
            if hasattr(analyzer, 'generate_personalized_suggestions'):
                suggestions = analyzer.generate_personalized_suggestions(ml_predictions, extracted_data, disadvantages)
            else:
                suggestions = analyzer.generate_suggestions(ml_predictions, extracted_data, disadvantages, overall_score)
        
        # === SECTION 1: SCORES ===
        st.markdown("<div class='section-header'>📊 Your Scores</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ats_score = ml_predictions.get('ats_score', 0) or 0
            ats_class = 'excellent' if ats_score >= 90 else 'good' if ats_score >= 75 else 'average' if ats_score >= 60 else 'poor'
            st.markdown(f"""
                <div class='score-card {ats_class}'>
                    <p class='score-number'>{ats_score:.0f}</p>
                    <p class='score-label'>ATS Score</p>
                    <p style='font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;'>
                        Applicant Tracking System compatibility
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            overall_class = 'excellent' if overall_score >= 90 else 'good' if overall_score >= 75 else 'average' if overall_score >= 60 else 'poor'
            st.markdown(f"""
                <div class='score-card {overall_class}'>
                    <p class='score-number'>{overall_score:.0f}</p>
                    <p class='score-label'>Overall Score</p>
                    <p style='font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;'>
                        Comprehensive resume quality
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            fraud_data = ml_predictions.get('fraud_detection', {})
            auth_score = fraud_data.get('authenticity_score', 100)
            auth_class = 'excellent' if auth_score >= 90 else 'good' if auth_score >= 75 else 'average' if auth_score >= 60 else 'poor'
            st.markdown(f"""
                <div class='score-card {auth_class}'>
                    <p class='score-number'>{auth_score:.0f}</p>
                    <p class='score-label'>Authenticity Score</p>
                    <p style='font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;'>
                        {fraud_data.get('verdict', 'Analyzing...')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Score Breakdown
        with st.expander("📈 Score Breakdown Details"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("ATS Compatibility", f"{score_breakdown['ats_score']:.0f}%", 
                         help="How well your resume passes automated screening")
                st.metric("Experience", f"{score_breakdown['experience']:.0f}%",
                         help="Based on years and positions")
            with col2:
                st.metric("Completeness", f"{score_breakdown['completeness']:.0f}%",
                         help="Contact info and essential sections")
                st.metric("Skills", f"{score_breakdown['skills']:.0f}%",
                         help="Technical skill diversity")
                         
        # === SECTION 2: PERSONAL DETAILS ===
        st.markdown("<div class='section-header'>👤 Personal Information</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("<p class='info-label'>Name</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-value'>{personal_details.get('name') or '❌ Not Found'}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("<p class='info-label'>Email</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-value'>{personal_details.get('email') or '❌ Not Found'}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("<p class='info-label'>Phone</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-value'>{personal_details.get('phone') or '❌ Not Found'}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("<p class='info-label'>Location</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-value'>{personal_details.get('location') or '❌ Not Found'}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("<p class='info-label'>LinkedIn</p>", unsafe_allow_html=True)
            linkedin = personal_details.get('linkedin')
            if linkedin:
                st.markdown(f"<p class='info-value'><a href='https://{linkedin}' target='_blank'>View Profile</a></p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='info-value'>❌ Not Found</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("<p class='info-label'>GitHub</p>", unsafe_allow_html=True)
            github = personal_details.get('github')
            if github:
                st.markdown(f"<p class='info-value'><a href='https://{github}' target='_blank'>View Profile</a></p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='info-value'>❌ Not Found</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # === SECTION 3: EXPERIENCE DETAILS ===
        st.markdown("<div class='section-header'>💼 Work Experience</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Experience", f"{experience_data.get('total_years', 0)} years")
        with col2:
            st.metric("Positions Held", experience_data.get('total_positions', 0))
        with col3:
            predicted_level = ml_predictions.get('experience_level', 'Unknown')
            st.metric("Experience Level", predicted_level)
        
        experiences = experience_data.get('experiences', [])
        if experiences:
            for exp in experiences:
                st.markdown(f"""
                    <div class='timeline-item'>
                        <div class='timeline-title'>{exp['role']}</div>
                        <div style='color: #667eea; font-weight: 600; margin: 0.3rem 0;'>{exp['company']}</div>
                        <div class='timeline-date'>{exp['duration']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No detailed work experience found in the resume. Consider adding specific positions with companies and dates.")
        
        # === SECTION 4: SKILLS ===
        st.markdown("<div class='section-header'>🛠️ Technical Skills</div>", unsafe_allow_html=True)
        
        technical_skills = skills_data.get('technical', {})
        if technical_skills:
            for category, skills in technical_skills.items():
                st.markdown(f"**{category}:**")
                st.markdown(" • ".join(skills))
                st.markdown("")
        else:
            st.warning("No technical skills detected. Make sure to include a clear skills section.")
        
        if skills_data.get('soft', []):
            st.markdown("**Soft Skills:**")
            st.markdown(" • ".join(skills_data['soft']))
        
        # Predicted Job Role
        predicted_role = ml_predictions.get('job_role')
        role_confidence = ml_predictions.get('role_confidence', 0)
        if predicted_role:
            st.info(f"🎯 **Predicted Best-Fit Role:** {predicted_role} (Confidence: {role_confidence}%)")
        
        # === SECTION 5: ADVANTAGES & DISADVANTAGES ===
        st.markdown("<div class='section-header'>⚖️ Strengths & Areas for Improvement</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Advantages")
            for category, items in advantages.items():
                st.markdown(f"**{category}:**")
                for item in items:
                    st.markdown(f"""
                        <div class='adv-card'>
                            ✓ {item}
                        </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚠️ Areas to Improve")
            for category, items in disadvantages.items():
                st.markdown(f"**{category}:**")
                for item in items:
                    st.markdown(f"""
                        <div class='dis-card'>
                            ✗ {item}
                        </div>
                    """, unsafe_allow_html=True)
        
        # === SECTION 6: PERSONALIZED SUGGESTIONS ===
        st.markdown("<div class='section-header'>💡 Personalized Recommendations</div>", unsafe_allow_html=True)
        
        st.markdown(f"**We've identified {len(suggestions)} actionable improvements to boost your resume score:**")
        st.markdown("")
        
        for i, suggestion in enumerate(suggestions, 1):
            priority_color = {
                'High': '🔴',
                'Medium': '🟡',
                'Low': '🟢'
            }
            
            st.markdown(f"""
                <div class='suggestion-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <strong>{priority_color[suggestion['priority']]} {suggestion['category']}</strong>
                            <span class='badge badge-info' style='margin-left: 0.5rem;'>{suggestion['priority']} Priority</span>
                        </div>
                        <span class='badge badge-success'>{suggestion['impact']}</span>
                    </div>
                    <p style='margin: 0.8rem 0 0 0; color: #1e293b;'>{suggestion['suggestion']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # === SECTION 7: ADDITIONAL INSIGHTS ===
        with st.expander("📚 Education & Projects"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Education:**")
                if education_data.get('degrees'):
                    for degree in education_data['degrees']:
                        st.markdown(f"• {degree}")
                else:
                    st.info("No education details found")
            
            with col2:
                st.markdown("**Projects:**")
                if projects:
                    for i, project in enumerate(projects, 1):
                        st.markdown(f"{i}. {project[:100]}...")
                else:
                    st.info("No projects found - consider adding them!")
        
        # Quality Tier
        quality_tier = ml_predictions.get('quality_tier')
        if quality_tier:
            st.info(f"📊 **Overall Quality Assessment:** {quality_tier}")
        
        # Download/Export options
        st.markdown("---")
        st.markdown("### 💾 Next Steps")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("📥 Download Report (PDF)", disabled=True, help="Coming soon!")
        with col2:
            st.button("📧 Email Report", disabled=True, help="Coming soon!")
        with col3:
            if st.button("🔄 Analyze Another Resume"):
                st.rerun()
        
        # Footer
        st.markdown("""
            <div class='footer'>
                <p>Made with ❤️ using AI & Machine Learning</p>
                <p style='font-size: 0.9rem; margin-top: 0.5rem;'>
                    Powered by Advanced NLP • 93%+ Accuracy • 2,500+ Training Samples
                </p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
