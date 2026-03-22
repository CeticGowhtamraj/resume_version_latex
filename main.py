# Add to your main app
from ml_predictor import get_predictor

# Initialize
ml_predictor = get_predictor()

# Make predictions
predictions = ml_predictor.get_all_predictions(resume_data, resume_text)

# Get results
ats_score = predictions['ats_score']
job_role = predictions['job_role']
is_fraud = predictions['fraud_detection']['is_fraud']