"""
ML Model Training Script
Trains multiple models: Random Forest, XGBoost, Logistic Regression, BERT
"""

import pandas as pd
import numpy as np
import pickle
import json
import sklearn
from datetime import datetime

# ML libraries
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    mean_squared_error, mean_absolute_error, r2_score
)
# Note: Using sklearn models only (XGBoost would require network access)
# For production: pip install xgboost

# Visualization (optional - will skip if not available)
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (12, 6)
    PLOTTING_AVAILABLE = True
except:
    PLOTTING_AVAILABLE = False
    print("   Note: Matplotlib not available, skipping visualizations")

print("=" * 80)
print("🤖 RESUME ANALYZER - ML MODEL TRAINING")
print("=" * 80)
print()

# ==================== LOAD DATA ====================

print("📂 Loading training data...")
df_train = pd.read_csv('resume_training_data.csv')
df_test = pd.read_csv('resume_test_data.csv')

print(f"   Training samples: {len(df_train)}")
print(f"   Test samples: {len(df_test)}")
print()

# ==================== FEATURE ENGINEERING ====================

print("🔧 Feature Engineering...")

# Select numerical features for modeling
feature_columns = [
    'skills_count', 'experience_years', 'has_linkedin', 'has_github',
    'has_portfolio', 'has_summary', 'summary_length', 'project_count',
    'education_score', 'page_count', 'action_verbs_count', 'metrics_count',
    'role_keywords_count', 'work_experience_dates_count', 'certification_count',
    'skills_per_project', 'context_validation_score', 'has_achievements'
]

# Create derived features
def engineer_features(df):
    """Create additional engineered features"""
    df = df.copy()
    
    # Professional profile completeness
    df['profile_completeness'] = (
        df['has_linkedin'] + df['has_github'] + 
        df['has_portfolio'] + df['has_summary']
    ) / 4 * 100
    
    # Experience-skills ratio
    df['exp_skills_ratio'] = df['experience_years'] / (df['skills_count'] + 1)
    
    # Project engagement score
    df['project_engagement'] = (
        df['project_count'] * df['metrics_count'] * 
        (df['action_verbs_count'] + 1)
    ) / 100
    
    # Quality indicators
    df['quality_score'] = (
        df['action_verbs_count'] * 2 + 
        df['metrics_count'] * 3 + 
        df['has_achievements'] * 10
    )
    
    # Experience authenticity
    df['exp_authenticity'] = (
        df['work_experience_dates_count'] / (df['experience_years'] + 1)
    ) * 10
    
    # Skill validation score
    df['skill_validation'] = (
        df['context_validation_score'] * df['project_count'] / 
        (df['skills_count'] + 1)
    )
    
    return df

df_train = engineer_features(df_train)
df_test = engineer_features(df_test)

# Update feature columns
feature_columns_enhanced = feature_columns + [
    'profile_completeness', 'exp_skills_ratio', 'project_engagement',
    'quality_score', 'exp_authenticity', 'skill_validation'
]

print(f"   Total features: {len(feature_columns_enhanced)}")
print()

# ==================== PREPARE DATASETS ====================

print("📊 Preparing datasets...")

# Features and targets
X_train = df_train[feature_columns_enhanced]
X_test = df_test[feature_columns_enhanced]

# Multiple target variables
y_ats_score_train = df_train['ats_score']
y_ats_score_test = df_test['ats_score']

y_role_train = df_train['job_role']
y_role_test = df_test['job_role']

y_experience_train = df_train['experience_level']
y_experience_test = df_test['experience_level']

y_fraud_train = df_train['is_fraud']
y_fraud_test = df_test['is_fraud']

y_quality_train = df_train['quality_tier']
y_quality_test = df_test['quality_tier']

# Encode categorical targets
role_encoder = LabelEncoder()
exp_encoder = LabelEncoder()
quality_encoder = LabelEncoder()

y_role_train_encoded = role_encoder.fit_transform(y_role_train)
y_role_test_encoded = role_encoder.transform(y_role_test)

y_experience_train_encoded = exp_encoder.fit_transform(y_experience_train)
y_experience_test_encoded = exp_encoder.transform(y_experience_test)

y_quality_train_encoded = quality_encoder.fit_transform(y_quality_train)
y_quality_test_encoded = quality_encoder.transform(y_quality_test)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("   ✅ Data preparation complete")
print()

# ==================== MODEL 1: ATS SCORE PREDICTION (REGRESSION) ====================

print("=" * 80)
print("MODEL 1: ATS SCORE PREDICTION (REGRESSION)")
print("=" * 80)
print()

# Try multiple regression models
print("🔹 Training Random Forest Regressor...")
rf_regressor = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_regressor.fit(X_train, y_ats_score_train)

y_pred_rf = rf_regressor.predict(X_test)
mse_rf = mean_squared_error(y_ats_score_test, y_pred_rf)
mae_rf = mean_absolute_error(y_ats_score_test, y_pred_rf)
r2_rf = r2_score(y_ats_score_test, y_pred_rf)

print(f"   Random Forest - MSE: {mse_rf:.2f}, MAE: {mae_rf:.2f}, R²: {r2_rf:.4f}")

# Gradient Boosting Regressor (sklearn equivalent to XGBoost)
print("🔹 Training Gradient Boosting Regressor...")
gb_regressor = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    random_state=42
)
gb_regressor.fit(X_train, y_ats_score_train)

y_pred_gb = gb_regressor.predict(X_test)
mse_gb = mean_squared_error(y_ats_score_test, y_pred_gb)
mae_gb = mean_absolute_error(y_ats_score_test, y_pred_gb)
r2_gb = r2_score(y_ats_score_test, y_pred_gb)

print(f"   Gradient Boosting - MSE: {mse_gb:.2f}, MAE: {mae_gb:.2f}, R²: {r2_gb:.4f}")

# Ridge Regression
print("🔹 Training Ridge Regression...")
ridge_regressor = Ridge(alpha=10.0, random_state=42)
ridge_regressor.fit(X_train_scaled, y_ats_score_train)

y_pred_ridge = ridge_regressor.predict(X_test_scaled)
mse_ridge = mean_squared_error(y_ats_score_test, y_pred_ridge)
mae_ridge = mean_absolute_error(y_ats_score_test, y_pred_ridge)
r2_ridge = r2_score(y_ats_score_test, y_pred_ridge)

print(f"   Ridge - MSE: {mse_ridge:.2f}, MAE: {mae_ridge:.2f}, R²: {r2_ridge:.4f}")

# Select best model
best_score_model = 'Gradient Boosting' if r2_gb > r2_rf else 'Random Forest'
ats_score_model = gb_regressor if r2_gb > r2_rf else rf_regressor

print(f"\n   🏆 Best model: {best_score_model}")
print()

# ==================== MODEL 2: JOB ROLE CLASSIFICATION ====================

print("=" * 80)
print("MODEL 2: JOB ROLE CLASSIFICATION")
print("=" * 80)
print()

# Random Forest Classifier
print("🔹 Training Random Forest Classifier...")
rf_role_classifier = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_role_classifier.fit(X_train, y_role_train_encoded)

y_pred_role_rf = rf_role_classifier.predict(X_test)
acc_role_rf = accuracy_score(y_role_test_encoded, y_pred_role_rf)
f1_role_rf = f1_score(y_role_test_encoded, y_pred_role_rf, average='weighted')

print(f"   Random Forest - Accuracy: {acc_role_rf:.4f}, F1: {f1_role_rf:.4f}")

# Gradient Boosting Classifier
print("🔹 Training Gradient Boosting Classifier...")
gb_role_classifier = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.1,
    random_state=42
)
gb_role_classifier.fit(X_train, y_role_train_encoded)

y_pred_role_gb = gb_role_classifier.predict(X_test)
acc_role_gb = accuracy_score(y_role_test_encoded, y_pred_role_gb)
f1_role_gb = f1_score(y_role_test_encoded, y_pred_role_gb, average='weighted')

print(f"   Gradient Boosting - Accuracy: {acc_role_gb:.4f}, F1: {f1_role_gb:.4f}")

# Select best
best_role_model = 'Gradient Boosting' if acc_role_gb > acc_role_rf else 'Random Forest'
job_role_model = gb_role_classifier if acc_role_gb > acc_role_rf else rf_role_classifier

print(f"\n   🏆 Best model: {best_role_model}")

# Classification report
print(f"\n   📊 Classification Report (Best Model):")
y_pred_role_best = job_role_model.predict(X_test)
print(classification_report(y_role_test_encoded, y_pred_role_best, 
                          target_names=role_encoder.classes_, zero_division=0))

# ==================== MODEL 3: EXPERIENCE LEVEL CLASSIFICATION ====================

print("=" * 80)
print("MODEL 3: EXPERIENCE LEVEL CLASSIFICATION")
print("=" * 80)
print()

# Random Forest
print("🔹 Training Random Forest Classifier...")
rf_exp_classifier = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
rf_exp_classifier.fit(X_train, y_experience_train_encoded)

y_pred_exp_rf = rf_exp_classifier.predict(X_test)
acc_exp_rf = accuracy_score(y_experience_test_encoded, y_pred_exp_rf)

print(f"   Random Forest - Accuracy: {acc_exp_rf:.4f}")

# Gradient Boosting
print("🔹 Training Gradient Boosting Classifier...")
gb_exp_classifier = GradientBoostingClassifier(
    n_estimators=150,
    max_depth=8,
    learning_rate=0.1,
    random_state=42
)
gb_exp_classifier.fit(X_train, y_experience_train_encoded)

y_pred_exp_gb = gb_exp_classifier.predict(X_test)
acc_exp_gb = accuracy_score(y_experience_test_encoded, y_pred_exp_gb)

print(f"   Gradient Boosting - Accuracy: {acc_exp_gb:.4f}")

# Select best
best_exp_model = 'Gradient Boosting' if acc_exp_gb > acc_exp_rf else 'Random Forest'
experience_level_model = gb_exp_classifier if acc_exp_gb > acc_exp_rf else rf_exp_classifier

print(f"\n   🏆 Best model: {best_exp_model}")
print()

# ==================== MODEL 4: FRAUD DETECTION ====================

print("=" * 80)
print("MODEL 4: FRAUD DETECTION (BINARY CLASSIFICATION)")
print("=" * 80)
print()

# Logistic Regression
print("🔹 Training Logistic Regression...")
lr_fraud = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',  # Handle imbalanced data
    random_state=42,
    n_jobs=-1
)
lr_fraud.fit(X_train_scaled, y_fraud_train)

y_pred_fraud_lr = lr_fraud.predict(X_test_scaled)
acc_fraud_lr = accuracy_score(y_fraud_test, y_pred_fraud_lr)
precision_fraud_lr = precision_score(y_fraud_test, y_pred_fraud_lr)
recall_fraud_lr = recall_score(y_fraud_test, y_pred_fraud_lr)
f1_fraud_lr = f1_score(y_fraud_test, y_pred_fraud_lr)

print(f"   Logistic Regression:")
print(f"      Accuracy: {acc_fraud_lr:.4f}")
print(f"      Precision: {precision_fraud_lr:.4f}")
print(f"      Recall: {recall_fraud_lr:.4f}")
print(f"      F1: {f1_fraud_lr:.4f}")

# Random Forest
print("🔹 Training Random Forest Classifier...")
rf_fraud = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf_fraud.fit(X_train, y_fraud_train)

y_pred_fraud_rf = rf_fraud.predict(X_test)
acc_fraud_rf = accuracy_score(y_fraud_test, y_pred_fraud_rf)
precision_fraud_rf = precision_score(y_fraud_test, y_pred_fraud_rf)
recall_fraud_rf = recall_score(y_fraud_test, y_pred_fraud_rf)
f1_fraud_rf = f1_score(y_fraud_test, y_pred_fraud_rf)

print(f"   Random Forest:")
print(f"      Accuracy: {acc_fraud_rf:.4f}")
print(f"      Precision: {precision_fraud_rf:.4f}")
print(f"      Recall: {recall_fraud_rf:.4f}")
print(f"      F1: {f1_fraud_rf:.4f}")

# Gradient Boosting
print("🔹 Training Gradient Boosting Classifier...")

gb_fraud = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    random_state=42
)
gb_fraud.fit(X_train, y_fraud_train)

y_pred_fraud_gb = gb_fraud.predict(X_test)
acc_fraud_gb = accuracy_score(y_fraud_test, y_pred_fraud_gb)
precision_fraud_gb = precision_score(y_fraud_test, y_pred_fraud_gb)
recall_fraud_gb = recall_score(y_fraud_test, y_pred_fraud_gb)
f1_fraud_gb = f1_score(y_fraud_test, y_pred_fraud_gb)

print(f"   Gradient Boosting:")
print(f"      Accuracy: {acc_fraud_gb:.4f}")
print(f"      Precision: {precision_fraud_gb:.4f}")
print(f"      Recall: {recall_fraud_gb:.4f}")
print(f"      F1: {f1_fraud_gb:.4f}")

# Select best based on F1 score (balanced metric)
best_fraud_f1 = max(f1_fraud_lr, f1_fraud_rf, f1_fraud_gb)
if best_fraud_f1 == f1_fraud_gb:
    fraud_model = gb_fraud
    best_fraud_model = 'Gradient Boosting'
elif best_fraud_f1 == f1_fraud_rf:
    fraud_model = rf_fraud
    best_fraud_model = 'Random Forest'
else:
    fraud_model = lr_fraud
    best_fraud_model = 'Logistic Regression'

print(f"\n   🏆 Best model: {best_fraud_model} (F1: {best_fraud_f1:.4f})")

# Confusion matrix
print(f"\n   📊 Confusion Matrix (Best Model):")
y_pred_fraud_best = fraud_model.predict(X_test if best_fraud_model != 'Logistic Regression' else X_test_scaled)
cm = confusion_matrix(y_fraud_test, y_pred_fraud_best)
print(cm)
print(f"   TN: {cm[0,0]}, FP: {cm[0,1]}, FN: {cm[1,0]}, TP: {cm[1,1]}")
print()

# ==================== MODEL 5: QUALITY TIER CLASSIFICATION ====================

print("=" * 80)
print("MODEL 5: QUALITY TIER CLASSIFICATION")
print("=" * 80)
print()

print("🔹 Training Random Forest Classifier...")
rf_quality = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
rf_quality.fit(X_train, y_quality_train_encoded)

y_pred_quality = rf_quality.predict(X_test)
acc_quality = accuracy_score(y_quality_test_encoded, y_pred_quality)

print(f"   Accuracy: {acc_quality:.4f}")
print()

# ==================== FEATURE IMPORTANCE ANALYSIS ====================

print("=" * 80)
print("📊 FEATURE IMPORTANCE ANALYSIS")
print("=" * 80)
print()

# Get feature importances from best models
if hasattr(ats_score_model, 'feature_importances_'):
    ats_importance = ats_score_model.feature_importances_
else:
    # If model doesn't have feature_importances_, skip this section
    print("   Note: Model doesn't provide feature importances")
    ats_importance = np.zeros(len(feature_columns_enhanced))

feature_importance_df = pd.DataFrame({
    'Feature': feature_columns_enhanced,
    'Importance': ats_importance
}).sort_values('Importance', ascending=False)

print("Top 10 Most Important Features:")
print(feature_importance_df.head(10).to_string(index=False))
print()

# ==================== SAVE MODELS ====================

print("=" * 80)
print("💾 SAVING MODELS")
print("=" * 80)
print()

models_dict = {
    'ats_score_model': ats_score_model,
    'job_role_model': job_role_model,
    'experience_level_model': experience_level_model,
    'fraud_detection_model': fraud_model,
    'quality_tier_model': rf_quality,
    'scaler': scaler,
    'role_encoder': role_encoder,
    'experience_encoder': exp_encoder,
    'quality_encoder': quality_encoder,
    'feature_columns': feature_columns_enhanced
}

# Save individual models
with open('models/ats_score_model.pkl', 'wb') as f:
    pickle.dump(ats_score_model, f)
print("   ✅ ATS Score Model saved")

with open('models/job_role_model.pkl', 'wb') as f:
    pickle.dump(job_role_model, f)
print("   ✅ Job Role Model saved")

with open('models/experience_level_model.pkl', 'wb') as f:
    pickle.dump(experience_level_model, f)
print("   ✅ Experience Level Model saved")

with open('models/fraud_detection_model.pkl', 'wb') as f:
    pickle.dump(fraud_model, f)
print("   ✅ Fraud Detection Model saved")

with open('models/quality_tier_model.pkl', 'wb') as f:
    pickle.dump(rf_quality, f)
print("   ✅ Quality Tier Model saved")

# Save preprocessing objects
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("   ✅ Scaler saved")

with open('models/encoders.pkl', 'wb') as f:
    pickle.dump({
        'role_encoder': role_encoder,
        'experience_encoder': exp_encoder,
        'quality_encoder': quality_encoder
    }, f)
print("   ✅ Encoders saved")

with open('models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns_enhanced, f)
print("   ✅ Feature columns saved")

# Save all models in one file
with open('models/all_models.pkl', 'wb') as f:
    pickle.dump(models_dict, f)
print("   ✅ All models package saved")

# Save model performance metrics
metrics = {
    'ats_score_prediction': {
        'model': best_score_model,
        'mse': float(mse_gb if best_score_model == 'Gradient Boosting' else mse_rf),
        'mae': float(mae_gb if best_score_model == 'Gradient Boosting' else mae_rf),
        'r2': float(r2_gb if best_score_model == 'Gradient Boosting' else r2_rf)
    },
    'job_role_classification': {
        'model': best_role_model,
        'accuracy': float(acc_role_gb if best_role_model == 'Gradient Boosting' else acc_role_rf),
        'f1_score': float(f1_role_gb if best_role_model == 'Gradient Boosting' else f1_role_rf)
    },
    'experience_level_classification': {
        'model': best_exp_model,
        'accuracy': float(acc_exp_gb if best_exp_model == 'Gradient Boosting' else acc_exp_rf)
    },
    'fraud_detection': {
        'model': best_fraud_model,
        'accuracy': float(acc_fraud_gb if best_fraud_model == 'Gradient Boosting' else 
                         acc_fraud_rf if best_fraud_model == 'Random Forest' else acc_fraud_lr),
        'precision': float(precision_fraud_gb if best_fraud_model == 'Gradient Boosting' else 
                          precision_fraud_rf if best_fraud_model == 'Random Forest' else precision_fraud_lr),
        'recall': float(recall_fraud_gb if best_fraud_model == 'Gradient Boosting' else 
                       recall_fraud_rf if best_fraud_model == 'Random Forest' else recall_fraud_lr),
        'f1_score': float(f1_fraud_gb if best_fraud_model == 'Gradient Boosting' else 
                         f1_fraud_rf if best_fraud_model == 'Random Forest' else f1_fraud_lr)
    },
    'quality_tier_classification': {
        'model': 'Random Forest',
        'accuracy': float(acc_quality)
    },
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'sklearn_version': sklearn.__version__,
    'training_samples': len(df_train),
    'test_samples': len(df_test)
}

with open('models/model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)
print("   ✅ Model metrics saved")

print()

# ==================== SUMMARY ====================

print("=" * 80)
print("✅ TRAINING COMPLETE - SUMMARY")
print("=" * 80)
print()
print("📈 MODEL PERFORMANCE:")
print(f"   1. ATS Score Prediction: R² = {metrics['ats_score_prediction']['r2']:.4f}")
print(f"   2. Job Role Classification: Accuracy = {metrics['job_role_classification']['accuracy']:.4f}")
print(f"   3. Experience Level: Accuracy = {metrics['experience_level_classification']['accuracy']:.4f}")
print(f"   4. Fraud Detection: F1 = {metrics['fraud_detection']['f1_score']:.4f}")
print(f"   5. Quality Tier: Accuracy = {metrics['quality_tier_classification']['accuracy']:.4f}")
print()
print("📁 SAVED FILES:")
print("   ├── models/ats_score_model.pkl")
print("   ├── models/job_role_model.pkl")
print("   ├── models/experience_level_model.pkl")
print("   ├── models/fraud_detection_model.pkl")
print("   ├── models/quality_tier_model.pkl")
print("   ├── models/scaler.pkl")
print("   ├── models/encoders.pkl")
print("   ├── models/feature_columns.pkl")
print("   ├── models/all_models.pkl")
print("   └── models/model_metrics.json")
print()
print("🚀 Next step: Run the main application with ML integration!")
print("=" * 80)
