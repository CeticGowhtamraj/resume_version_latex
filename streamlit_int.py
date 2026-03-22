import streamlit as st
from ml_predictor import get_predictor
import PyPDF2
import docx

def extract_text_from_file(uploaded_file):
    text = ""

    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


st.title("🤖 AI Resume Analyzer")

predictor = get_predictor()

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF/DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    try:
        text = extract_text_from_file(uploaded_file)

        resume_data = {
                 "skills": [],
                "experience_years": 0,
                "no_of_pages": 1
}


        predictions = predictor.get_all_predictions(resume_data, text)

        st.success("Analysis Complete ✅")

        # Safe access
        ats_score = predictions.get('ats_score', "Not Available")

        st.metric("ATS Score", ats_score)

        st.write("Full Predictions:")
        st.write(predictions)

    except Exception as e:
        st.error("Something went wrong:")
        st.write(e)


def generate_suggestions(features):
    suggestions = []

    if features['skills_count'] < 5:
        suggestions.append("Add more relevant technical skills.")

    if features['metrics_count'] == 0:
        suggestions.append("Add measurable achievements (e.g., Improved performance by 30%).")

    if features['has_summary'] == 0:
        suggestions.append("Include a professional summary section.")

    if features['has_linkedin'] == 0:
        suggestions.append("Add your LinkedIn profile link.")

    if features['project_count'] < 2:
        suggestions.append("Include at least 2 strong projects.")

    if features['action_verbs_count'] < 3:
        suggestions.append("Use strong action verbs like 'Developed', 'Led', 'Built'.")

    return suggestions

st.title("🤖 AI-Powered Resume Analyzer")

predictor = get_predictor()

