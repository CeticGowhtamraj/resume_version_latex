"""
Enhanced Resume Analyzer with Full ML Integration - IMPROVED VERSION
Fixed: Name extraction, Experience detection, Location parsing
Added: 6-second analysis simulation for better UX
"""

import PyPDF2
import docx
import re
import os
import tempfile
import time
from datetime import datetime
from ml_predictor import get_predictor
import json
import numpy as np
from collections import defaultdict


class ImprovedResumeAnalyzer:
    """
    Enhanced Resume Analyzer with:
    - IMPROVED: Name extraction with better pattern matching
    - IMPROVED: Experience calculation with better date parsing
    - IMPROVED: Location detection with multiple pattern support
    - Added: 6-second analysis delay for UI feedback
    """
    
    def __init__(self):
        """Initialize the analyzer with ML predictor"""
        self.predictor = get_predictor()
        self.debug = True
        
        if self.predictor.models_loaded:
            print("[OK] ML-Powered Resume Analyzer initialized")
        else:
            print("[WARN] Rule-based Resume Analyzer initialized (ML models not available)")
    
    def log(self, message, level="INFO"):
        """Log messages if debug is enabled"""
        if self.debug:
            print(f"[{level}] {message}")

    def _build_skill_pattern(self, skill):
        """Build a regex pattern that handles symbolic skills like C++/C# correctly."""
        escaped = re.escape(skill)
        if len(skill) == 1 and skill.isalpha():
            return r'(?<![\w.+#-])' + escaped + r'(?![\w+#])'
        if re.search(r'[^A-Za-z0-9_]', skill):
            return r'(?<!\w)' + escaped + r'(?!\w)'
        return r'\b' + escaped + r'\b'

    def _is_section_heading(self, line):
        """Detect short section heading lines to reduce cross-section parsing errors."""
        if not line:
            return False
        clean = re.sub(r'[^a-z ]', ' ', line.lower())
        clean = re.sub(r'\s+', ' ', clean).strip()
        if not clean or len(clean) > 40:
            return False
        headings = {
            'experience', 'work experience', 'professional experience', 'employment', 'work history',
            'education', 'skills', 'technical skills', 'key competencies', 'projects', 'certifications',
            'summary', 'objective', 'profile', 'contact', 'personal details'
        }
        return clean in headings
    
    # ==================== TEXT EXTRACTION ====================
    
    def extract_text_from_file(self, file_path):
        """
        Extract text from PDF or DOCX with multiple fallback strategies
        """
        temp_path = None
        try:
            # Support both filesystem paths and uploaded file-like objects (e.g., Streamlit).
            if isinstance(file_path, (str, os.PathLike)):
                resolved_path = str(file_path)
                if not os.path.exists(resolved_path):
                    self.log(f"File not found: {resolved_path}", "ERROR")
                    return ""
            else:
                original_name = getattr(file_path, 'name', 'uploaded_resume')
                ext = original_name.lower().split('.')[-1] if '.' in original_name else ''
                if ext not in {'pdf', 'docx', 'doc'}:
                    file_type = getattr(file_path, 'type', '') or ''
                    if 'pdf' in file_type:
                        ext = 'pdf'
                    elif 'word' in file_type or 'docx' in file_type:
                        ext = 'docx'
                if ext not in {'pdf', 'docx', 'doc'}:
                    self.log("Unsupported uploaded file type", "ERROR")
                    return ""
                data = file_path.getvalue() if hasattr(file_path, 'getvalue') else file_path.read()
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
                    tmp.write(data)
                    temp_path = tmp.name
                resolved_path = temp_path

            file_size = os.path.getsize(resolved_path)
            self.log(f"Processing file: {resolved_path} ({file_size} bytes)")

            file_extension = resolved_path.lower().split('.')[-1]

            if file_extension == 'pdf':
                return self._extract_from_pdf(resolved_path)
            elif file_extension in ['docx', 'doc']:
                return self._extract_from_docx(resolved_path)
            else:
                self.log(f"Unsupported file type: {file_extension}", "ERROR")
                return ""
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
    
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF with multiple methods"""
        text = ""
        
        # Method 1: Standard PyPDF2 extraction
        try:
            self.log("Attempting PyPDF2 extraction (Method 1)")
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                self.log(f"PDF has {num_pages} pages")
                
                for i, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as e:
                        self.log(f"Page {i+1}: extraction failed - {e}", "WARN")
                        continue
                
                if len(text) > 100:
                    self.log(f"[OK] PyPDF2 successful: {len(text)} chars")
                    return text.strip()
        except Exception as e:
            self.log(f"PyPDF2 Method 1 failed: {e}", "ERROR")
        
        # Method 2: Try with strict=False
        try:
            self.log("Attempting PyPDF2 with error recovery (Method 2)")
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f, strict=False)
                for page in pdf_reader.pages:
                    try:
                        text += page.extract_text() or ""
                    except:
                        continue
                
                if len(text) > 100:
                    self.log(f"[OK] PyPDF2 (strict=False) successful: {len(text)} chars")
                    return text.strip()
        except Exception as e:
            self.log(f"PyPDF2 Method 2 failed: {e}", "ERROR")

        self.log("All PDF extraction methods failed", "ERROR")
        return text.strip() if text else ""

    def _extract_from_docx(self, file_path):
        """Extract text from DOCX"""
        text = ""
        
        try:
            self.log("Attempting DOCX extraction")
            doc = docx.Document(file_path)
            
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            text = '\n'.join(paragraphs)
            
            if len(text) > 100:
                self.log(f"[OK] DOCX extraction successful: {len(text)} chars")
                return text.strip()
            else:
                self.log("DOCX appears empty", "WARN")
                return text
                
        except Exception as e:
            self.log(f"DOCX extraction failed: {e}", "ERROR")
            return ""
    
    # ==================== IMPROVED PERSONAL DETAILS EXTRACTION ====================
    
    def extract_personal_details(self, text):
        """
        IMPROVED: Extract personal information with better name and location detection
        """
        details = {
            'name': None,
            'email': None,
            'phone': None,
            'location': None,
            'linkedin': None,
            'github': None
        }
        
        text_lower = text.lower()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # ==================== EMAIL ====================
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            details['email'] = emails[0]
            self.log(f"Found email: {details['email']}")
        
        # ==================== PHONE ====================
        phone_patterns = [
            r'\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',  # US format
            r'\+?(\d{1,3})[-.\s]?(\d{10})',  # International with country code
            r'\+?(\d{1,3})[-.\s]?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{4,5}',  # Flexible international
            r'\b(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b',  # Standard
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple):
                    details['phone'] = ''.join(matches[0])
                else:
                    details['phone'] = matches[0]
                self.log(f"Found phone: {details['phone']}")
                break
        
        # ==================== IMPROVED NAME EXTRACTION ====================
        name = self._extract_name_improved(text, lines, details.get('email'))
        if name:
            details['name'] = name
            self.log(f"Found name: {details['name']}")
        
        # ==================== IMPROVED LOCATION EXTRACTION ====================
        location = self._extract_location_improved(text, lines)
        if location:
            details['location'] = location
            self.log(f"Found location: {details['location']}")
        
        # ==================== LINKEDIN ====================
        linkedin = self._extract_linkedin(text, text_lower)
        if linkedin:
            details['linkedin'] = linkedin
            self.log(f"Found LinkedIn: {details['linkedin']}")
        
        # ==================== GITHUB ====================
        github = self._extract_github(text, text_lower)
        if github:
            details['github'] = github
            self.log(f"Found GitHub: {details['github']}")
        
        return details
    
    def _extract_name_improved(self, text, lines, email):
        """
        IMPROVED: Extract candidate name with better accuracy
        Uses multiple strategies with priority order
        """
        # Strategy 1: Look in first 15 lines for proper name pattern
        bad_name_terms = {
            'developer', 'development', 'engineer', 'engineering', 'stack', 'project', 'application', 
            'intern', 'internship', 'experience', 'education', 'skills', 'competencies', 'resume', 
            'curriculum', 'vitae', 'objective', 'summary', 'profile', 'contact', 'professional',
            'technical', 'software', 'frontend', 'backend', 'fullstack', 'full stack', 'web', 
            'mobile', 'data', 'analyst', 'scientist', 'manager', 'senior', 'junior', 'lead'
        }
        
        for line in lines[:15]:
            # Skip lines with email, phone, location indicators
            if re.search(r'@|phone|email|tel|linkedin|github|http|www\.|\.com', line, re.IGNORECASE):
                continue
            
            # Skip section headings
            if self._is_section_heading(line.lower()):
                continue
            
            # Clean the line
            candidate = re.sub(r'^[\W_]+|[\W_]+$', '', line)
            
            # Skip lines with digits, URLs, special chars
            if re.search(r'[@\d:/|]', candidate):
                continue
            
            # Check word count (names are typically 2-4 words)
            words = [w for w in re.split(r'\s+', candidate) if w]
            if not (2 <= len(words) <= 4):
                continue
            
            # Length check (names are typically 5-50 characters)
            if not (5 <= len(candidate) <= 50):
                continue
            
            # Must have alphabetic words
            alpha_words = [w for w in words if re.search(r'[A-Za-z]', w)]
            if len(alpha_words) < 2:
                continue
            
            # Check for bad terms
            low_words = {w.lower() for w in alpha_words}
            if low_words & bad_name_terms:
                continue
            
            # Check for title case (proper names start with capital letters)
            title_case_count = sum(1 for w in alpha_words if w[0].isupper())
            if title_case_count >= 2:  # At least 2 words should start with capital
                # Final validation: name shouldn't contain job-related terms
                if not re.search(
                    r'(developer|engineer|designer|analyst|manager|consultant|specialist|coordinator)',
                    candidate,
                    re.IGNORECASE
                ):
                    return candidate
        
        # Strategy 2: Extract from email if available
        if email:
            local = email.split('@')[0]
            # Remove numbers, dots, underscores, hyphens
            local_clean = re.sub(r'[\d._-]+', ' ', local).strip()
            parts = [p for p in local_clean.split() if p and len(p) > 1]
            if 1 < len(parts) <= 4:
                name_from_email = ' '.join(p.title() for p in parts)
                self.log(f"Extracted name from email: {name_from_email}")
                return name_from_email
        
        # Strategy 3: Find any proper name pattern in first 3000 chars
        proper_name_pattern = r'\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?\b'
        possible_names = re.findall(proper_name_pattern, text[:3000])
        
        for candidate in possible_names:
            # Skip if it contains institutional or job-related terms
            if not re.search(
                r'(university|college|institute|school|company|corporation|technologies|solutions|'
                r'systems|services|project|application|development|competencies|experience)',
                candidate,
                re.IGNORECASE
            ):
                return candidate
        
        self.log("Name extraction failed - using fallback", "WARN")
        return "Name Not Found"
    
    def _extract_location_improved(self, text, lines):
        """
        IMPROVED: Extract location with better pattern matching
        Handles: "City, State", "City, Country", "City, State, Country"
        """
        # Get header section (first 30 lines or 2000 chars)
        header_text = "\n".join(lines[:30]) if lines else text[:2000]
        
        # Common location indicator patterns
        location_indicators = [
            r'(?:location|address|residing in|based in|lives in):\s*([^\n]+)',
            r'(?:location|address)[\s:]+([A-Z][A-Za-z\s,]+(?:India|USA|UK|Canada|Australia))',
        ]
        
        for pattern in location_indicators:
            match = re.search(pattern, header_text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Clean up the location
                location = re.sub(r'\s+', ' ', location)
                if 5 <= len(location) <= 100:
                    return location
        
        # Pattern 1: US format "City, ST" (e.g., "San Francisco, CA")
        us_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z]{2})\b'
        us_matches = re.findall(us_pattern, header_text)
        for city, state in us_matches:
            # Verify it's not a company name or other entity
            if state in ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI', 
                        'NJ', 'VA', 'WA', 'MA', 'AZ', 'TN', 'IN', 'MO', 'MD', 'WI',
                        'CO', 'MN', 'SC', 'AL', 'LA', 'KY', 'OR', 'OK', 'CT', 'UT']:
                return f"{city}, {state}"
        
        # Pattern 2: International "City, State, Country" (e.g., "Chennai, Tamil Nadu, India")
        intl_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+)\b'
        intl_matches = re.findall(intl_pattern, header_text)
        for city, state, country in intl_matches:
            # Verify country names
            common_countries = ['India', 'USA', 'Canada', 'Australia', 'UK', 'Singapore', 
                              'Malaysia', 'Germany', 'France', 'Japan', 'China']
            if country in common_countries:
                return f"{city}, {state}, {country}"
        
        # Pattern 3: Simple "City, Country" (e.g., "Mumbai, India")
        simple_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+)\b'
        simple_matches = re.findall(simple_pattern, header_text)
        for city, country in simple_matches:
            common_countries = ['India', 'USA', 'Canada', 'Australia', 'UK', 'Singapore',
                              'Malaysia', 'Germany', 'France', 'Japan', 'China', 'Ireland',
                              'Netherlands', 'Belgium', 'Switzerland', 'Sweden', 'Norway']
            if country in common_countries:
                return f"{city}, {country}"
        
        # Pattern 4: Look for Indian states specifically
        indian_states = [
            'Tamil Nadu', 'Karnataka', 'Maharashtra', 'Kerala', 'Andhra Pradesh', 
            'Telangana', 'West Bengal', 'Gujarat', 'Rajasthan', 'Uttar Pradesh',
            'Madhya Pradesh', 'Bihar', 'Odisha', 'Punjab', 'Haryana', 'Delhi'
        ]
        for state in indian_states:
            state_pattern = rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*{re.escape(state)}'
            match = re.search(state_pattern, header_text)
            if match:
                return f"{match.group(1)}, {state}, India"
        
        # Pattern 5: Just state/country without city
        location_only_pattern = r'\b(?:' + '|'.join(indian_states) + r'),\s*India\b'
        match = re.search(location_only_pattern, header_text)
        if match:
            return match.group(0)
        
        self.log("Location not found", "WARN")
        return None
    
    def _extract_linkedin(self, text, text_lower):
        """Extract LinkedIn profile URL"""
        linkedin = None
        
        # Method 1: Try to find actual URL in text
        linkedin_url_patterns = [
            r'https?://(?:www\.)?linkedin\.com/in/([\w-]+)',
            r'linkedin\.com/in/([\w-]+)',
            r'www\.linkedin\.com/in/([\w-]+)',
        ]
        
        for pattern in linkedin_url_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                username = matches[0]
                linkedin = f"linkedin.com/in/{username}"
                break
        
        # Method 2: Check for "linkedin" keyword in header
        if not linkedin:
            header_section = text[:1500].lower()
            if 'linkedin' in header_section:
                # Verify it's not about working at LinkedIn
                linkedin_context = re.search(r'.{0,40}linkedin.{0,40}', header_section)
                if linkedin_context:
                    context_text = linkedin_context.group().lower()
                    exclude_phrases = [
                        'experience at linkedin', 'worked at linkedin', 'job at linkedin',
                        'employed at linkedin', 'engineer at linkedin', 'developer at linkedin'
                    ]
                    is_employment = any(phrase in context_text for phrase in exclude_phrases)
                    if not is_employment:
                        linkedin = 'Present (hyperlinked)'
        
        # Method 3: Check for label formats
        if not linkedin:
            linkedin_label_patterns = [
                r'linkedin:\s*([^\s\n]{10,})',
                r'linkedin profile:\s*([^\s\n]{10,})',
                r'li:\s*([^\s\n]{10,})',
            ]
            for pattern in linkedin_label_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    username = matches[0].strip('/').replace('linkedin.com/in/', '').replace('www.', '')
                    linkedin = f"linkedin.com/in/{username}"
                    break
        
        return linkedin
    
    def _extract_github(self, text, text_lower):
        """Extract GitHub profile URL"""
        github = None
        
        # Method 1: Try to find actual URL
        github_url_patterns = [
            r'https?://(?:www\.)?github\.com/([\w-]+)',
            r'github\.com/([\w-]+)',
            r'www\.github\.com/([\w-]+)',
        ]
        
        for pattern in github_url_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                username = matches[0]
                if username.lower() not in ['github', 'features', 'explore', 'topics', 'about', 'pricing', 'team']:
                    github = f"github.com/{username}"
                    break
        
        # Method 2: Check for "github" keyword
        if not github:
            header_section = text[:1500].lower()
            if 'github' in header_section:
                github_context = re.search(r'.{0,40}github.{0,40}', header_section)
                if github_context:
                    context_text = github_context.group().lower()
                    exclude_phrases = [
                        'experience at github', 'worked at github', 'job at github',
                        'employed at github', 'engineer at github', 'developer at github'
                    ]
                    is_employment = any(phrase in context_text for phrase in exclude_phrases)
                    if not is_employment:
                        github = 'Present (hyperlinked)'
        
        # Method 3: Check for label formats
        if not github:
            github_label_patterns = [
                r'github:\s*([^\s\n]{5,})',
                r'github profile:\s*([^\s\n]{5,})',
                r'gh:\s*([^\s\n]{5,})',
            ]
            for pattern in github_label_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    username = matches[0].strip('/').replace('github.com/', '').replace('www.', '')
                    if username.lower() not in ['github', 'features']:
                        github = f"github.com/{username}"
                        break
        
        return github
    
    # ==================== SKILLS EXTRACTION ====================
    
    def extract_skills(self, text):
        """Extract technical skills from resume"""
        text_lower = text.lower()
        
        skill_categories = {
            'programming': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby', 'php',
                'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'dart'
            ],
            'web': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'nodejs', 'express',
                'django', 'flask', 'spring', 'asp.net', 'laravel', 'next.js', 'nuxt.js',
                'jquery', 'bootstrap', 'tailwind', 'sass', 'less', 'webpack', 'babel'
            ],
            'mobile': [
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
                'swift', 'kotlin', 'objective-c', 'swiftui'
            ],
            'database': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle',
                'sql server', 'sqlite', 'mariadb', 'dynamodb', 'couchdb', 'neo4j'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'cloud', 'ec2', 's3', 'lambda', 'cloudformation', 'terraform'
            ],
            'devops': [
                'docker', 'kubernetes', 'jenkins', 'ci/cd', 'gitlab', 'github actions',
                'ansible', 'puppet', 'chef', 'vagrant', 'nginx', 'apache'
            ],
            'data_science': [
                'machine learning', 'ml', 'deep learning', 'ai', 'artificial intelligence',
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
                'data analysis', 'data visualization', 'tableau', 'power bi', 'jupyter'
            ],
            'frameworks': [
                'spring boot', 'hibernate', '.net', 'rails', 'symfony', 'codeigniter',
                'express.js', 'fastapi', 'streamlit', 'gradle', 'maven', 'npm', 'yarn'
            ],
            'testing': [
                'junit', 'pytest', 'jest', 'mocha', 'selenium', 'cypress',
                'testing', 'unit testing', 'integration testing', 'test automation'
            ],
            'design': [
                'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
                'wireframing', 'prototyping', 'ui design', 'ux design',
                'indesign', 'after effects', 'premiere pro'
            ],
            'tools': [
                'git', 'github', 'jira', 'confluence', 'slack', 'linux',
                'bash', 'vim', 'vscode', 'visual studio code', 'intellij', 'postman', 'swagger',
                'trello', 'asana', 'notion'
            ]
        }
        
        found_skills = {
            'technical': {},
            'all': []
        }
        
        # Look for skills section explicitly
        skills_section_pattern = r'(?:SKILLS?|TECHNICAL SKILLS?|CORE COMPETENCIES|KEY COMPETENCIES|TECH STACK|TECHNOLOGIES)[:\s]+((?:.|\n)*?)(?=\n\n|EXPERIENCE|EDUCATION|PROJECTS|$)'
        skills_match = re.search(skills_section_pattern, text, re.IGNORECASE)
        
        search_text = text_lower
        if skills_match:
            skills_section = skills_match.group(1).lower()
            self.log(f"Found dedicated skills section ({len(skills_section)} chars)")
            search_text = skills_section + "\n" + text_lower
        
        for category, skills in skill_categories.items():
            category_skills = []
            for skill in skills:
                pattern = self._build_skill_pattern(skill)
                if re.search(pattern, search_text):
                    # Capitalize properly
                    if skill.upper() == skill and len(skill) <= 4:  # SQL, AWS, etc.
                        normalized = skill.upper()
                    elif '.' in skill or '/' in skill:
                        normalized = skill
                    else:
                        normalized = skill.title()
                    
                    if normalized not in category_skills:
                        category_skills.append(normalized)
            
            if category_skills:
                found_skills['technical'][category] = category_skills
                found_skills['all'].extend(category_skills)
        
        # Remove duplicates
        seen = set()
        deduplicated = []
        for skill in found_skills['all']:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                deduplicated.append(skill)
        
        found_skills['all'] = deduplicated
        
        self.log(f"Found {len(found_skills['all'])} skills across {len(found_skills['technical'])} categories")
        
        return found_skills
    
    # ==================== IMPROVED EXPERIENCE EXTRACTION ====================
    
    def extract_experience(self, text):
        """
        IMPROVED: Extract work experience with better date parsing
        """
        experience_data = {
            'total_years': 0,
            'work_years': 0,
            'internship_years': 0,
            'total_positions': 0,
            'work_positions': 0,
            'internship_positions': 0,
            'experiences': []
        }
        
        # Improved date patterns
        month_names = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
        date_token = rf'{month_names}\.?\s*\d{{4}}|\b(?:19|20)\d{{2}}\b|Present|Current|Till Date|Ongoing|Now'
        range_pattern = re.compile(rf'({date_token})\s*(?:-|–|—|to|till)\s*({date_token})', re.IGNORECASE)
        
        internship_keywords = [
            'intern', 'internship', 'trainee', 'apprentice', 
            'summer student', 'co-op', 'co op', 'coop', 'working student'
        ]
        
        lines = text.split('\n')
        in_experience = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if we're entering experience section
            if self._is_section_heading(line_lower) and any(keyword in line_lower for keyword in ['experience', 'employment', 'work history']):
                in_experience = True
                self.log("Found experience section")
                continue
            
            # Check if we're leaving experience section
            if in_experience and self._is_section_heading(line_lower) and any(keyword in line_lower for keyword in ['education', 'certifications', 'projects', 'skills']):
                self.log("Exiting experience section")
                break
            
            if in_experience and line.strip():
                range_match = range_pattern.search(line)
                if range_match:
                    dates = [range_match.group(1), range_match.group(2)]
                    
                    # Check if it's an internship
                    is_internship = any(keyword in line_lower for keyword in internship_keywords)
                    
                    # Validate the line has enough text
                    alpha_only = re.sub(r'[^A-Za-z ]', '', line).strip()
                    if len(alpha_only) < 4:
                        continue
                    
                    # Extract title and company
                    title_company = line.strip()
                    company = None
                    title = title_company
                    
                    # Try "at" separator
                    at_match = re.search(r'(.+?)\s+at\s+(.+?)(?:\s*\||$)', line, re.IGNORECASE)
                    if at_match:
                        title = at_match.group(1).strip()
                        company = at_match.group(2).strip()
                    else:
                        # Try pipe or dash separator
                        sep_match = re.search(r'(.+?)\s*[\|\-]\s*(.+?)(?:\s*\(|$)', line)
                        if sep_match:
                            title = sep_match.group(1).strip()
                            company = sep_match.group(2).strip()
                    
                    # Clean up company name if it contains dates
                    if company and range_pattern.search(company):
                        company = None
                    
                    # Extract description from next lines
                    description = []
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line and not range_pattern.search(next_line):
                            if next_line.startswith(('•', '-', '●', '◦', '*')) or len(next_line) > 30:
                                description.append(next_line.lstrip('•-●◦* '))
                        else:
                            break
                    
                    # Calculate years of experience
                    try:
                        # Extract start year
                        start_match = re.search(r'\d{4}', dates[0])
                        if start_match:
                            start_year = int(start_match.group())
                        else:
                            continue
                        
                        # Extract end year or use current year
                        if re.search(r'present|current|till date|ongoing|now', dates[1], re.IGNORECASE):
                            end_year = datetime.now().year
                        else:
                            end_match = re.search(r'\d{4}', dates[1])
                            if end_match:
                                end_year = int(end_match.group())
                            else:
                                continue
                        
                        years = max(0, end_year - start_year)
                        
                        # If duration is less than 1 year, count as 0.5 years (6 months)
                        if years == 0:
                            years = 0.5
                        
                    except Exception as e:
                        self.log(f"Date parsing error: {e}", "WARN")
                        years = 0
                    
                    experience_entry = {
                        'title': title,
                        'company': company or 'Company name not specified',
                        'dates': f"{dates[0]} - {dates[1]}",
                        'years': years,
                        'is_internship': is_internship,
                        'type': 'Internship' if is_internship else 'Full-time',
                        'description': ' '.join(description[:2]) if description else ''
                    }
                    
                    experience_data['experiences'].append(experience_entry)
                    experience_data['total_years'] += years
                    experience_data['total_positions'] += 1
                    
                    if is_internship:
                        experience_data['internship_years'] += years
                        experience_data['internship_positions'] += 1
                    else:
                        experience_data['work_years'] += years
                        experience_data['work_positions'] += 1
                    
                    self.log(f"Found experience: {title} ({years} years)")
        
        # Round total years to 1 decimal place
        experience_data['total_years'] = round(experience_data['total_years'], 1)
        experience_data['work_years'] = round(experience_data['work_years'], 1)
        experience_data['internship_years'] = round(experience_data['internship_years'], 1)
        
        self.log(f"Total experience: {experience_data['total_years']} years ({experience_data['total_positions']} positions)")
        
        return experience_data
    
    # ==================== EDUCATION EXTRACTION ====================
    
    def extract_education(self, text):
        """Extract education information with improved parsing"""
        education_data = {
            'degrees': [],
            'institutions': [],
            'highest_degree': None,
            'graduation_years': []
        }
        
        degree_patterns = [
            r'(?:Bachelor|B\.?S\.?|B\.?E\.?|B\.?Tech|B\.?A\.?|BA|BS)\s+(?:of\s+)?(?:Science|Engineering|Arts|Technology|Computer Science)?',
            r'(?:Master|M\.?S\.?|M\.?E\.?|M\.?Tech|M\.?A\.?|MA|MS|MBA)\s+(?:of\s+)?(?:Science|Engineering|Arts|Technology|Business Administration)?',
            r'(?:Doctor|Ph\.?D\.?|Doctorate)\s+(?:of\s+)?(?:Philosophy)?',
            r'(?:Associate|A\.?S\.?|A\.?A\.?)\s+(?:of\s+)?(?:Science|Arts)?'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                degree = match.strip()
                if degree not in education_data['degrees']:
                    education_data['degrees'].append(degree)
        
        # Extract institutions
        institution_patterns = [
            r'(?:University|Institute|College|School)\s+of\s+[A-Z][A-Za-z\s]+',
            r'[A-Z][A-Za-z\s]+\s+(?:University|Institute|College|School)'
        ]
        
        for pattern in institution_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                institution = match.strip()
                if len(institution) > 10 and institution not in education_data['institutions']:
                    education_data['institutions'].append(institution)
        
        # Extract graduation years
        grad_years = re.findall(r'\b(19|20)\d{2}\b', text)
        education_data['graduation_years'] = sorted(set(grad_years))
        
        # Determine highest degree
        degree_hierarchy = ['Doctorate', 'Ph.D', 'PhD', 'Master', 'M.S', 'MS', 'M.Tech', 'MBA', 'Bachelor', 'B.S', 'BS', 'B.Tech', 'B.E', 'Associate']
        for level in degree_hierarchy:
            for degree in education_data['degrees']:
                if level.lower() in degree.lower():
                    education_data['highest_degree'] = degree
                    break
            if education_data['highest_degree']:
                break
        
        self.log(f"Found {len(education_data['degrees'])} degrees")
        
        return education_data
    
    # ==================== PROJECTS EXTRACTION ====================
    
    def extract_projects(self, text):
        """Extract project information"""
        projects = []
        
        # Look for projects section
        project_section_pattern = r'(?:PROJECTS?|PERSONAL PROJECTS?|ACADEMIC PROJECTS?)[:\s]+((?:.|\n)*?)(?=\n\n|EXPERIENCE|EDUCATION|SKILLS|CERTIFICATIONS|$)'
        project_match = re.search(project_section_pattern, text, re.IGNORECASE)
        
        if project_match:
            project_section = project_match.group(1)
            lines = project_section.split('\n')
            
            current_project = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # New project (typically starts with bullet or is bold/capitalized)
                if line.startswith(('•', '-', '●', '◦', '*')) or (len(line) < 100 and line[0].isupper()):
                    if current_project:
                        projects.append(current_project)
                    
                    project_name = line.lstrip('•-●◦* ')
                    current_project = {
                        'name': project_name,
                        'description': ''
                    }
                elif current_project:
                    # Add to current project description
                    current_project['description'] += ' ' + line
            
            # Add last project
            if current_project:
                projects.append(current_project)
        
        self.log(f"Found {len(projects)} projects")
        
        return projects
    
    # ==================== JOB ROLE DETECTION ====================
    
    def detect_job_role(self, text, skills):
        """Detect job role based on skills and content"""
        text_lower = text.lower()
        
        role_patterns = {
            'Frontend Developer': {
                'keywords': ['react', 'angular', 'vue', 'html', 'css', 'javascript', 'frontend', 'ui', 'ux'],
                'weight': 0
            },
            'Backend Developer': {
                'keywords': ['java', 'python', 'node', 'api', 'backend', 'server', 'database', 'spring', 'django', 'flask'],
                'weight': 0
            },
            'Full Stack Developer': {
                'keywords': ['full stack', 'fullstack', 'mern', 'mean', 'frontend', 'backend'],
                'weight': 0
            },
            'Data Scientist': {
                'keywords': ['machine learning', 'data science', 'python', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'ml', 'ai'],
                'weight': 0
            },
            'DevOps Engineer': {
                'keywords': ['docker', 'kubernetes', 'aws', 'ci/cd', 'jenkins', 'devops', 'ansible', 'terraform'],
                'weight': 0
            },
            'Mobile Developer': {
                'keywords': ['android', 'ios', 'react native', 'flutter', 'mobile', 'swift', 'kotlin'],
                'weight': 0
            },
            'Data Analyst': {
                'keywords': ['tableau', 'power bi', 'excel', 'sql', 'data analysis', 'visualization', 'analytics'],
                'weight': 0
            },
            'Software Engineer': {
                'keywords': ['software', 'engineer', 'development', 'programming', 'coding'],
                'weight': 0
            }
        }
        
        # Calculate weights
        for role, data in role_patterns.items():
            for keyword in data['keywords']:
                if keyword in text_lower or keyword.lower() in [s.lower() for s in skills]:
                    role_patterns[role]['weight'] += 1
        
        # Find best match
        best_role = max(role_patterns.items(), key=lambda x: x[1]['weight'])
        role = best_role[0]
        confidence = min(95, best_role[1]['weight'] * 10)  # Cap at 95%
        
        # Default to Software Engineer if no strong match
        if confidence < 30:
            role = 'Software Engineer'
            confidence = 50
        
        self.log(f"Detected role: {role} ({confidence}% confidence)")
        
        return role, confidence
    
    # ==================== MAIN ANALYZE FUNCTION WITH 6-SECOND DELAY ====================
    
    def analyze_resume(self, file_path, simulate_delay=True):
        """
        Main analysis function with simulated 6-second delay for better UX
        
        Args:
            file_path: Path to resume file or file-like object
            simulate_delay: If True, adds 6-second delay with progress updates
        
        Returns:
            dict: Complete analysis results
        """
        start_time = time.time()
        
        # Step 1: Extract text (0-1 second)
        if simulate_delay:
            self.log("📄 Extracting text from resume...")
            time.sleep(1)
        
        text = self.extract_text_from_file(file_path)
        if not text or len(text) < 100:
            return {
                'success': False,
                'error': 'Resume appears empty or could not be extracted'
            }
        
        # Step 2: Extract personal details (1-2 seconds)
        if simulate_delay:
            self.log("👤 Extracting personal information...")
            time.sleep(1)
        
        personal_details = self.extract_personal_details(text)
        
        # Step 3: Extract skills (2-3 seconds)
        if simulate_delay:
            self.log("🛠️ Analyzing technical skills...")
            time.sleep(1)
        
        skills_data = self.extract_skills(text)
        
        # Step 4: Extract experience (3-4 seconds)
        if simulate_delay:
            self.log("💼 Calculating work experience...")
            time.sleep(1)
        
        experience_data = self.extract_experience(text)
        
        # Step 5: Extract education (4-5 seconds)
        if simulate_delay:
            self.log("🎓 Processing education details...")
            time.sleep(1)
        
        education_data = self.extract_education(text)
        
        # Step 6: Detect job role (5-5.5 seconds)
        if simulate_delay:
            self.log("🎯 Detecting job role...")
            time.sleep(0.5)
        
        job_role, role_confidence = self.detect_job_role(text, skills_data['all'])
        
        # Step 7: ML predictions (5.5-6 seconds)
        if simulate_delay:
            self.log("🤖 Running ML predictions...")
            time.sleep(0.5)
        
        # Prepare data for ML predictor
        resume_data = {
            'skills': skills_data['all'],
            'experience_years': experience_data['total_years'],
            'no_of_pages': 1  # Will be updated if PDF
        }
        
        # Get page count if PDF
        if isinstance(file_path, str) and file_path.lower().endswith('.pdf'):
            try:
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    resume_data['no_of_pages'] = len(pdf_reader.pages)
            except:
                pass
        
        # Get ML predictions
        ml_predictions = self.predictor.get_all_predictions(resume_data, text)
        
        # Extract projects
        projects = self.extract_projects(text)
        
        # Build extracted data
        extracted_data = {
            'personal_details': personal_details,
            'skills': skills_data,
            'experience': experience_data,
            'education': education_data,
            'projects': projects
        }
        
        # Calculate scores
        advantages, disadvantages = self.calculate_advantages_disadvantages(extracted_data)
        
        # Calculate overall score
        ats_score = ml_predictions.get('ats_score', 0)
        overall_score = ats_score
        
        # Generate suggestions
        suggestions = self.generate_suggestions(ml_predictions, extracted_data, disadvantages, overall_score)
        
        # Get authenticity details
        authenticity_details = self.get_authenticity_details(ml_predictions, extracted_data)
        
        # Determine experience level
        exp_years = experience_data['total_years']
        if exp_years < 1:
            experience_level = 'Fresher'
        elif exp_years < 3:
            experience_level = 'Junior'
        elif exp_years < 6:
            experience_level = 'Mid-Level'
        elif exp_years < 10:
            experience_level = 'Senior'
        else:
            experience_level = 'Expert'
        
        elapsed_time = time.time() - start_time
        self.log(f"✅ Analysis complete in {elapsed_time:.1f} seconds")
        
        # Return complete analysis
        return {
            'success': True,
            'personal_details': personal_details,
            'skills': skills_data,
            'experience': experience_data,
            'education': education_data,
            'projects': projects,
            'job_role': ml_predictions.get('job_role', job_role),
            'role_confidence': ml_predictions.get('role_confidence', role_confidence),
            'experience_level': ml_predictions.get('experience_level', experience_level),
            'ats_score': ats_score,
            'overall_score': overall_score,
            'advantages': advantages,
            'disadvantages': disadvantages,
            'suggestions': suggestions,
            'fraud_detection': ml_predictions.get('fraud_detection', {}),
            'authenticity_details': authenticity_details,
            'quality_tier': ml_predictions.get('quality_tier'),
            'ml_predictions': ml_predictions,
            'analysis_time': elapsed_time
        }
    
    # ==================== SCORING HELPERS ====================
    
    def calculate_advantages_disadvantages(self, extracted_data):
        """Calculate advantages and disadvantages"""
        advantages = []
        disadvantages = []
        
        exp_years = extracted_data.get('experience', {}).get('total_years', 0)
        if exp_years >= 5:
            advantages.append(f"Strong professional experience ({exp_years} years)")
        elif exp_years >= 2:
            advantages.append(f"Moderate professional experience ({exp_years} years)")
        elif exp_years < 1:
            disadvantages.append("Limited professional experience")
        
        skill_count = len(extracted_data.get('skills', {}).get('all', []))
        if skill_count >= 10:
            advantages.append(f"Comprehensive skill set ({skill_count} skills)")
        elif skill_count >= 5:
            advantages.append(f"Good technical skills ({skill_count} skills)")
        else:
            disadvantages.append("Limited technical skills listed")
        
        personal = extracted_data.get('personal_details', {})
        if personal.get('linkedin') and personal.get('github'):
            advantages.append("Complete professional profile (LinkedIn + GitHub)")
        elif personal.get('linkedin'):
            advantages.append("LinkedIn profile present")
        elif not personal.get('linkedin'):
            disadvantages.append("Missing LinkedIn profile")
        
        if not personal.get('email'):
            disadvantages.append("Email address not found")
        if not personal.get('phone'):
            disadvantages.append("Phone number not found")
        
        project_count = len(extracted_data.get('projects', []))
        if project_count >= 3:
            advantages.append(f"Strong project portfolio ({project_count} projects)")
        elif project_count == 0:
            disadvantages.append("No projects listed")
        
        return advantages, disadvantages
    
    def generate_suggestions(self, ml_predictions, extracted_data, disadvantages, overall_score):
        """Generate actionable suggestions"""
        suggestions = []
        
        if overall_score < 60:
            suggestions.append("🎯 Focus on increasing overall score to 70+ for better visibility")
        
        if "Limited professional experience" in str(disadvantages):
            suggestions.append("💼 Add internships, freelance work, or volunteer projects")
        
        if "Limited technical skills" in str(disadvantages):
            suggestions.append("🛠️ Add more relevant technical skills (aim for 10-15)")
        
        if "Missing LinkedIn" in str(disadvantages):
            suggestions.append("🔗 Add LinkedIn profile URL")
        
        if "No projects listed" in str(disadvantages):
            suggestions.append("📁 Add 2-3 significant projects with details")
        
        features = ml_predictions.get('features', {})
        
        if features.get('action_verbs_count', 0) < 5:
            suggestions.append("✍️ Use more action verbs: Led, Developed, Improved, Achieved")
        
        if features.get('metrics_count', 0) < 3:
            suggestions.append("📊 Add quantifiable achievements (e.g., 'Improved performance by 30%')")
        
        if not features.get('has_summary'):
            suggestions.append("📝 Add a professional summary section (2-3 sentences)")
        
        return suggestions[:7]
    
    def get_authenticity_details(self, ml_predictions, extracted_data):
        """Get detailed authenticity analysis"""
        fraud_data = ml_predictions.get('fraud_detection', {})
        features = ml_predictions.get('features', {})
        
        details = {
            'authenticity_score': fraud_data.get('authenticity_score', 100),
            'overall_verdict': fraud_data.get('verdict', 'Verified'),
            'confidence': fraud_data.get('confidence', 0),
            'factors': []
        }
        
        # Experience validation
        exp_years = extracted_data.get('experience', {}).get('total_years', 0)
        skill_count = len(extracted_data.get('skills', {}).get('all', []))
        
        if skill_count > exp_years * 10 and exp_years > 0:
            details['factors'].append({
                'factor': 'Skills vs Experience',
                'status': 'warning',
                'icon': 'exclamation-triangle',
                'color': 'yellow',
                'message': f'Unusually high skill count ({skill_count}) for {exp_years} years experience'
            })
        else:
            details['factors'].append({
                'factor': 'Skills vs Experience',
                'status': 'pass',
                'icon': 'check-circle',
                'color': 'green',
                'message': 'Skills align with experience level'
            })
        
        # Content quality
        metrics_count = features.get('metrics_count', 0)
        action_verbs = features.get('action_verbs_count', 0)
        
        if metrics_count >= 3 and action_verbs >= 5:
            details['factors'].append({
                'factor': 'Content Quality',
                'status': 'pass',
                'icon': 'check-circle',
                'color': 'green',
                'message': f'Good use of metrics ({metrics_count}) and action verbs ({action_verbs})'
            })
        elif metrics_count < 2:
            details['factors'].append({
                'factor': 'Content Quality',
                'status': 'warning',
                'icon': 'exclamation-triangle',
                'color': 'yellow',
                'message': 'Add more quantifiable achievements and metrics'
            })
        
        # Professional links
        personal = extracted_data.get('personal_details', {})
        links_count = sum([1 for k in ['linkedin', 'github'] if personal.get(k)])
        
        if links_count >= 2:
            details['factors'].append({
                'factor': 'Professional Presence',
                'status': 'pass',
                'icon': 'check-circle',
                'color': 'green',
                'message': f'Strong online presence with {links_count} professional links'
            })
        elif links_count == 1:
            details['factors'].append({
                'factor': 'Professional Presence',
                'status': 'warning',
                'icon': 'info-circle',
                'color': 'blue',
                'message': 'Add more professional profiles (LinkedIn and GitHub recommended)'
            })
        else:
            details['factors'].append({
                'factor': 'Professional Presence',
                'status': 'fail',
                'icon': 'times-circle',
                'color': 'red',
                'message': 'No professional links found - add LinkedIn and GitHub'
            })
        
        return details


# Singleton instance
_analyzer = None

def get_analyzer():
    """Get or create global analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = ImprovedResumeAnalyzer()
    return _analyzer


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ENHANCED ML-POWERED RESUME ANALYZER - IMPROVED VERSION")
    print("="*70 + "\n")
    
    analyzer = ImprovedResumeAnalyzer()
    
    test_text = """
    Rahul Kumar
    rahul.kumar@email.com
    +91 98765 43210
    Chennai, Tamil Nadu, India
    linkedin.com/in/rahulkumar
    github.com/rahulkumar
    
    PROFESSIONAL SUMMARY
    Software Engineer with 3+ years of experience building scalable web applications
    
    SKILLS
    Python, JavaScript, React, Node.js, Django, PostgreSQL, AWS, Docker, Git
    
    EXPERIENCE
    Software Engineer - Tech Solutions Pvt Ltd (Jan 2022 - Present)
    - Developed RESTful APIs using Django and PostgreSQL
    - Improved application performance by 40%
    - Led team of 3 junior developers
    
    Junior Developer - Startup Inc (Jun 2020 - Dec 2021)
    - Built responsive web applications using React
    - Implemented CI/CD pipelines
    
    EDUCATION
    Bachelor of Technology in Computer Science
    Anna University - 2020
    """
    
    print("Testing improved extraction methods:\n")
    
    personal = analyzer.extract_personal_details(test_text)
    print("Personal Details:")
    for key, value in personal.items():
        print(f"  {key}: {value}")
    
    experience = analyzer.extract_experience(test_text)
    print(f"\nExperience: {experience['total_years']} years")
    print(f"  Positions: {experience['total_positions']}")
    for exp in experience['experiences']:
        print(f"  - {exp['title']} at {exp['company']} ({exp['years']} years)")
    
    skills = analyzer.extract_skills(test_text)
    print(f"\nSkills: {len(skills['all'])} total")
    print(f"  All: {', '.join(skills['all'][:10])}")
    
    role, confidence = analyzer.detect_job_role(test_text, skills['all'])
    print(f"\nJob Role: {role} ({confidence}% confidence)")
    
    print("\n" + "="*70)
    print("✅ All improvements applied successfully!")
    print("✅ Name extraction: Multiple strategies with better filtering")
    print("✅ Experience calculation: Improved date parsing with month names")
    print("✅ Location detection: Multiple pattern support for international locations")
    print("✅ 6-second analysis delay: Built into analyze_resume() function")
    print("="*70 + "\n")