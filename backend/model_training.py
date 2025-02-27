"""import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
class EducationLevelProcessor:
    def __init__(self, level_name):
        self.level_name = level_name
        self.specialization_encoder = LabelEncoder()
        self.pathway_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Define level-specific pathways
        self.pathway_mappings = {
            'SSLC': ['Science PU', 'Commerce PU', 'Arts PU', 'ITI', 'Diploma'],
            'PU': ['Engineering', 'Medical', 'Commerce', 'Arts', 'Computer Applications'],
            'Diploma': ['BE/BTech', 'Industry Job', 'Advanced Diploma'],
            'ITI': ['Industry Job', 'Advanced Training', 'Entrepreneurship'],
            'Bachelors': ['Masters in Tech', 'MBA', 'Industry Job', 'Research', 'Higher Studies Abroad'],
            'Masters': ['Research/PhD', 'Industry Leadership', 'Academia', 'Entrepreneurship']
        }
        
        # Define level-specific features
        self.feature_configs = {
            'SSLC': ['science_marks', 'maths_marks', 'english_marks', 'total_marks'],
            'PU': ['stream', 'physics_marks', 'chemistry_marks', 'maths_marks', 'percentage'],
            'Diploma': ['branch', 'core_subjects_avg', 'project_score', 'percentage'],
            'ITI': ['trade', 'practical_score', 'theory_score', 'percentage'],
            'Bachelors': ['branch', 'cgpa', 'project_score', 'internship_rating'],
            'Masters': ['specialization', 'cgpa', 'research_score', 'publication_count']
        }
        
        self.pathways = self.pathway_mappings[level_name]

    def generate_synthetic_data(self, n_samples=1000):
        np.random.seed(42)
        
        data = []
        for _ in range(n_samples):
            record = self._generate_level_specific_record()
            record['recommended_pathway'] = self._assign_pathway(record)
            data.append(record)
            
        return pd.DataFrame(data)
    
    def _generate_level_specific_record(self):
        if self.level_name == 'SSLC':
            return {
                'science_marks': np.random.randint(50, 100),
                'maths_marks': np.random.randint(50, 100),
                'english_marks': np.random.randint(50, 100),
                'total_marks': 0  # Will be calculated
            }
        elif self.level_name == 'PU':
            return {
                'stream': np.random.choice(['Science', 'Commerce', 'Arts']),
                'physics_marks': np.random.randint(60, 100),
                'chemistry_marks': np.random.randint(60, 100),
                'maths_marks': np.random.randint(60, 100),
                'percentage': 0  # Will be calculated
            }
        elif self.level_name == 'Diploma':
            return {
                'branch': np.random.choice(['CS', 'ME', 'EE', 'CE']),
                'core_subjects_avg': np.random.uniform(60, 95),
                'project_score': np.random.uniform(70, 100),
                'percentage': np.random.uniform(60, 95)
            }
        elif self.level_name == 'ITI':
            return {
                'trade': np.random.choice(['Electrician', 'Mechanic', 'Welder', 'Fitter']),
                'practical_score': np.random.uniform(70, 100),
                'theory_score': np.random.uniform(60, 95),
                'percentage': np.random.uniform(60, 95)
            }
        elif self.level_name == 'Bachelors':
            return {
                'branch': np.random.choice(['CS', 'IT', 'ME', 'EE', 'CE']),
                'cgpa': np.random.uniform(6, 10),
                'project_score': np.random.uniform(70, 100),
                'internship_rating': np.random.uniform(3, 5)
            }
        else:  # Masters
            return {
                'specialization': np.random.choice(['AI/ML', 'Data Science', 'IoT', 'VLSI', 'Power Systems']),
                'cgpa': np.random.uniform(7, 10),
                'research_score': np.random.uniform(75, 100),
                'publication_count': np.random.randint(0, 4)
            }

    def _assign_pathway(self, record):
        # Level-specific pathway assignment logic
        if self.level_name == 'SSLC':
            total_marks = sum([record['science_marks'], record['maths_marks'], record['english_marks']])
            if total_marks >= 250:
                return np.random.choice(['Science PU', 'Diploma'])
            elif total_marks >= 200:
                return np.random.choice(['Commerce PU', 'ITI'])
            else:
                return 'Arts PU'
        
        elif self.level_name == 'PU':
            percentage = np.mean([record['physics_marks'], record['chemistry_marks'], record['maths_marks']])
            if percentage >= 85:
                return 'Engineering'
            elif percentage >= 75:
                return np.random.choice(['Medical', 'Computer Applications'])
            else:
                return np.random.choice(['Commerce', 'Arts'])
        
        # Similar logic for other levels...
        return np.random.choice(self.pathways)

    def prepare_features(self, df):
        # Encode categorical columns if they exist
        feature_df = df.copy()
        categorical_columns = ['stream', 'branch', 'trade', 'specialization']
        
        for col in categorical_columns:
            if col in feature_df.columns:
                feature_df[f'{col}_encoded'] = self.specialization_encoder.fit_transform(feature_df[col])
        
        # Select numerical columns
        numerical_cols = [col for col in self.feature_configs[self.level_name] 
                        if col in feature_df.columns and feature_df[col].dtype in ['int64', 'float64']]
        
        # Combine encoded categorical and numerical features
        encoded_cols = [col for col in feature_df.columns if col.endswith('_encoded')]
        features = feature_df[numerical_cols + encoded_cols].values
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        return features_scaled

    def save_model_artifacts(self, model, base_path):
        # Create level-specific directory
        level_path = f"{base_path}/{self.level_name.lower()}"
        os.makedirs(level_path, exist_ok=True)
        
        # Save model and encoders
        joblib.dump(model, f"{level_path}/model.joblib")
        joblib.dump(self.specialization_encoder, f"{level_path}/specialization_encoder.joblib")
        joblib.dump(self.pathway_encoder, f"{level_path}/pathway_encoder.joblib")
        joblib.dump(self.scaler, f"{level_path}/scaler.joblib")

def train_level_specific_model(level_name, base_path='models'):
    processor = EducationLevelProcessor(level_name)
    df = processor.generate_synthetic_data()
    
    X = processor.prepare_features(df)
    y = processor.pathway_encoder.fit_transform(df['recommended_pathway'])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model with optimized parameters
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42
    )
    
    # Perform cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f'{level_name} Cross-validation accuracy: {np.mean(cv_scores):.2f}')
    
    # Train and evaluate
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    
    print(f"\n{level_name} Model Performance:")
    print(f"Test accuracy: {accuracy_score(y_test, y_pred_test):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_test, 
                              target_names=processor.pathway_encoder.classes_))
    
    # Save model artifacts
    processor.save_model_artifacts(model, base_path)
    
    return model, processor

def train_all_models():
    education_levels = ['SSLC', 'PU', 'Diploma', 'ITI', 'Bachelors', 'Masters']
    models = {}
    
    for level in education_levels:
        print(f"\nTraining model for {level}...")
        model, processor = train_level_specific_model(level)
        models[level] = (model, processor)
    
    return models

if __name__ == '__main__':
    models = train_all_models()"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class EducationLevelProcessor:
    def __init__(self, level_name):
        self.level_name = level_name
        self.specialization_encoder = LabelEncoder()
        self.pathway_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Define level-specific pathways
        self.pathway_mappings = {
            'SSLC': ['Science PU', 'Commerce PU', 'Arts PU', 'ITI', 'Diploma'],
            'PU': ['Engineering', 'Medical', 'Commerce', 'Arts', 'Computer Applications'],
            'Diploma': ['BE/BTech', 'Industry Job', 'Advanced Diploma'],
            'ITI': ['Industry Job', 'Advanced Training', 'Entrepreneurship'],
            'Bachelors': ['Masters in Tech', 'MBA', 'Industry Job', 'Research', 'Higher Studies Abroad'],
            'Masters': ['Research/PhD', 'Industry Leadership', 'Academia', 'Entrepreneurship']
        }
        
        # Define level-specific features
        self.feature_configs = {
            'SSLC': ['science_marks', 'maths_marks', 'english_marks', 'total_marks'],
            'PU': ['stream', 'physics_marks', 'chemistry_marks', 'maths_marks', 'percentage'],
            'Diploma': ['branch', 'core_subjects_avg', 'project_score', 'percentage'],
            'ITI': ['trade', 'practical_score', 'theory_score', 'percentage'],
            'Bachelors': ['branch', 'cgpa', 'project_score', 'internship_rating'],
            'Masters': ['specialization', 'cgpa', 'research_score', 'publication_count']
        }
        
        self.pathways = self.pathway_mappings[level_name]

    def generate_balanced_data(self, n_samples=1000):
        np.random.seed(42)
        data = []
        samples_per_pathway = n_samples // len(self.pathways)

        for pathway in self.pathways:
            for _ in range(samples_per_pathway):
                record = self._generate_level_specific_record()
                record['recommended_pathway'] = pathway
                data.append(record)
                
        return pd.DataFrame(data)

    def _generate_level_specific_record(self):
        if self.level_name == 'SSLC':
            return {
                'science_marks': np.random.randint(60, 100),
                'maths_marks': np.random.randint(60, 100),
                'english_marks': np.random.randint(60, 100),
                'total_marks': 0  # Will be calculated
            }
        elif self.level_name == 'PU':
            return {
                'stream': np.random.choice(['Science', 'Commerce', 'Arts']),
                'physics_marks': np.random.randint(60, 100),
                'chemistry_marks': np.random.randint(60, 100),
                'maths_marks': np.random.randint(60, 100),
                'percentage': 0  # Will be calculated
            }
        elif self.level_name == 'Diploma':
            return {
                'branch': np.random.choice(['CS', 'ME', 'EE', 'CE']),
                'core_subjects_avg': np.random.uniform(70, 95),
                'project_score': np.random.uniform(80, 100),
                'percentage': np.random.uniform(70, 95)
            }
        elif self.level_name == 'ITI':
            return {
                'trade': np.random.choice(['Electrician', 'Mechanic', 'Welder', 'Fitter']),
                'practical_score': np.random.uniform(75, 100),
                'theory_score': np.random.uniform(70, 95),
                'percentage': np.random.uniform(70, 95)
            }
        elif self.level_name == 'Bachelors':
            return {
                'branch': np.random.choice(['CS', 'IT', 'ME', 'EE', 'CE']),
                'cgpa': np.random.uniform(7, 10),
                'project_score': np.random.uniform(80, 100),
                'internship_rating': np.random.uniform(4, 5)
            }
        else:  # Masters
            return {
                'specialization': np.random.choice(['AI/ML', 'Data Science', 'IoT', 'VLSI', 'Power Systems']),
                'cgpa': np.random.uniform(8, 10),
                'research_score': np.random.uniform(80, 100),
                'publication_count': np.random.randint(1, 5)
            }

    def prepare_features(self, df):
        feature_df = df.copy()
        categorical_columns = ['stream', 'branch', 'trade', 'specialization']

        for col in categorical_columns:
            if col in feature_df.columns:
                feature_df[f'{col}_encoded'] = self.specialization_encoder.fit_transform(feature_df[col])

        numerical_cols = [col for col in self.feature_configs[self.level_name] 
                          if col in feature_df.columns and feature_df[col].dtype in ['int64', 'float64']]

        encoded_cols = [col for col in feature_df.columns if col.endswith('_encoded')]
        features = feature_df[numerical_cols + encoded_cols].values

        features_scaled = self.scaler.fit_transform(features)
        return features_scaled

    def save_model_artifacts(self, model, base_path):
        level_path = f"{base_path}/{self.level_name.lower()}"
        os.makedirs(level_path, exist_ok=True)

        joblib.dump(model, f"{level_path}/model.joblib")
        joblib.dump(self.specialization_encoder, f"{level_path}/specialization_encoder.joblib")
        joblib.dump(self.pathway_encoder, f"{level_path}/pathway_encoder.joblib")
        joblib.dump(self.scaler, f"{level_path}/scaler.joblib")


def train_level_specific_model(level_name, base_path='models'):
    processor = EducationLevelProcessor(level_name)
    df = processor.generate_balanced_data()

    X = processor.prepare_features(df)
    y = processor.pathway_encoder.fit_transform(df['recommended_pathway'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42
    )

    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f'{level_name} Cross-validation accuracy: {np.mean(cv_scores):.2f}')

    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)

    print(f"\n{level_name} Model Performance:")
    print(f"Test accuracy: {accuracy_score(y_test, y_pred_test):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_test, 
                                target_names=processor.pathway_encoder.classes_))

    processor.save_model_artifacts(model, base_path)

    return model, processor


def train_all_models():
    education_levels = ['SSLC', 'PU', 'Diploma', 'ITI', 'Bachelors', 'Masters']
    models = {}

    for level in education_levels:
        print(f"\nTraining model for {level}...")
        model, processor = train_level_specific_model(level)
        models[level] = (model, processor)

    return models


if __name__ == '__main__':
    models = train_all_models()
