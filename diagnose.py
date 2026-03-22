#!/usr/bin/env python3
"""
Resume Analyzer - Diagnostic Script
Checks all requirements and identifies issues
"""

import sys
import os
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_python_version():
    print_header("Python Version Check")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print_info(f"Python version: {version_str}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python version OK (3.8+ required)")
        return True
    else:
        print_error(f"Python 3.8+ required, found {version_str}")
        return False

def check_dependencies():
    print_header("Dependency Check")
    
    required = {
        'flask': 'Flask',
        'PyPDF2': 'PyPDF2',
        'docx': 'python-docx',
        'sklearn': 'scikit-learn',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'streamlit': 'streamlit (optional)'
    }
    
    all_ok = True
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print_success(f"{package:25s} installed")
        except ImportError:
            if module == 'streamlit':
                print_warning(f"{package:25s} not installed (optional)")
            else:
                print_error(f"{package:25s} NOT INSTALLED")
                missing.append(package)
                all_ok = False
    
    if missing:
        print(f"\n{Colors.YELLOW}Install missing packages:{Colors.END}")
        print(f"pip install {' '.join(missing)} --break-system-packages")
    
    return all_ok

def check_files():
    print_header("File Check")
    
    required_files = {
        'app.py': 'Flask backend',
        'improved_analyzer.py': 'Analyzer logic',
        'ml_predictor.py': 'ML predictor',
        'generate_training_data.py': 'Data generator',
        'train_models.py': 'Model trainer',
        'index.html': 'Frontend HTML',
        'script.js': 'Frontend JavaScript'
    }
    
    all_ok = True
    
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print_success(f"{filename:30s} ({description})")
        else:
            # Check for renamed files
            if filename == 'index.html':
                if os.path.exists('1770879519367_index.html'):
                    print_warning(f"{filename:30s} found as '1770879519367_index.html' - NEEDS RENAME")
                    all_ok = False
                else:
                    print_error(f"{filename:30s} MISSING ({description})")
                    all_ok = False
            elif filename == 'script.js':
                if os.path.exists('1770879509565_script.js'):
                    print_warning(f"{filename:30s} found as '1770879509565_script.js' - NEEDS RENAME")
                    all_ok = False
                else:
                    print_error(f"{filename:30s} MISSING ({description})")
                    all_ok = False
            else:
                print_error(f"{filename:30s} MISSING ({description})")
                all_ok = False
    
    return all_ok

def check_models():
    print_header("ML Models Check")
    
    if not os.path.exists('models'):
        print_error("models/ directory NOT FOUND")
        print_info("Run: python3 generate_training_data.py")
        print_info("Then: python3 train_models.py")
        return False
    
    required_models = [
        'ats_score_model.pkl',
        'job_role_model.pkl',
        'experience_level_model.pkl',
        'fraud_detection_model.pkl',
        'quality_tier_model.pkl',
        'scaler.pkl',
        'encoders.pkl',
        'feature_columns.pkl'
    ]
    
    all_ok = True
    found_count = 0
    
    for model_file in required_models:
        path = os.path.join('models', model_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            size_kb = size / 1024
            print_success(f"{model_file:30s} ({size_kb:.1f} KB)")
            found_count += 1
        else:
            print_error(f"{model_file:30s} MISSING")
            all_ok = False
    
    print(f"\nFound {found_count}/{len(required_models)} model files")
    
    if not all_ok:
        print_info("Run: python3 train_models.py")
    
    return all_ok

def check_data_files():
    print_header("Data Files Check")
    
    if os.path.exists('resume_training_data.csv'):
        size = os.path.getsize('resume_training_data.csv')
        size_kb = size / 1024
        print_success(f"resume_training_data.csv ({size_kb:.1f} KB)")
        return True
    else:
        print_warning("resume_training_data.csv NOT FOUND")
        print_info("Run: python3 generate_training_data.py")
        return False

def test_imports():
    print_header("Import Test")
    
    try:
        print_info("Testing imports...")
        from improved_analyzer import ImprovedResumeAnalyzer
        print_success("improved_analyzer imports OK")
        
        from ml_predictor import get_predictor
        print_success("ml_predictor imports OK")
        
        return True
    except Exception as e:
        print_error(f"Import failed: {str(e)}")
        return False

def check_port():
    print_header("Port Check")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print_warning("Port 5000 is already in use")
            print_info("Run: lsof -ti:5000 | xargs kill -9")
            print_info("Or change port in app.py")
            return False
        else:
            print_success("Port 5000 is available")
            return True
    except Exception as e:
        print_warning(f"Could not check port: {str(e)}")
        return True

def print_summary(checks):
    print_header("Summary")
    
    total = len(checks)
    passed = sum(checks.values())
    failed = total - passed
    
    print(f"Total Checks: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    print()
    
    if all(checks.values()):
        print_success("All checks passed! ✨")
        print()
        print("You can now run:")
        print("  python3 app.py")
        print()
        print("Then open: http://localhost:5000")
    else:
        print_error("Some checks failed. Fix the issues above.")
        print()
        print("Quick fixes:")
        print("  1. Install dependencies: pip install Flask PyPDF2 python-docx scikit-learn numpy pandas --break-system-packages")
        print("  2. Rename files: mv 1770879519367_index.html index.html && mv 1770879509565_script.js script.js")
        print("  3. Generate data: python3 generate_training_data.py")
        print("  4. Train models: python3 train_models.py")
        print()
        print("Or run: bash setup.sh")

def main():
    print_header("Resume Analyzer - Diagnostic Tool")
    
    checks = {}
    
    checks['python'] = check_python_version()
    checks['dependencies'] = check_dependencies()
    checks['files'] = check_files()
    checks['data'] = check_data_files()
    checks['models'] = check_models()
    checks['imports'] = test_imports()
    checks['port'] = check_port()
    
    print_summary(checks)

if __name__ == '__main__':
    main()