from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Dictionary to store level-specific models and processors
models = {}
education_levels = ['SSLC', 'PU', 'Diploma', 'ITI', 'Bachelors', 'Masters']

# Load models and processors for each education level
for level in education_levels:
    level_path = f"models/{level.lower()}"
    try:
        models[level] = {
            'model': joblib.load(f"{level_path}/model.joblib"),
            'specialization_encoder': joblib.load(f"{level_path}/specialization_encoder.joblib"),
            'pathway_encoder': joblib.load(f"{level_path}/pathway_encoder.joblib"),
            'scaler': joblib.load(f"{level_path}/scaler.joblib")
        }
    except Exception as e:
        print(f"Error loading models for {level}: {e}")

# Configure OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def prepare_features(data, level):
    """Convert input data to model features based on education level"""
    model_data = models.get(level)
    if not model_data:
        raise ValueError(f"No model found for education level: {level}")

    features = []
    if level == 'SSLC':
        features = [
            data.get('science_marks', 0),
            data.get('maths_marks', 0),
            data.get('english_marks', 0),
            sum([data.get('science_marks', 0), 
                 data.get('maths_marks', 0), 
                 data.get('english_marks', 0)])
        ]
    elif level == 'PU':
        stream_encoded = model_data['specialization_encoder'].transform([data.get('stream', 'Science')])[0]
        features = [
            stream_encoded,
            data.get('physics_marks', 0),
            data.get('chemistry_marks', 0),
            data.get('maths_marks', 0),
            data.get('percentage', 0)
        ]
    elif level == 'Diploma':
        branch_encoded = model_data['specialization_encoder'].transform([data.get('branch', 'CS')])[0]
        features = [
            branch_encoded,
            data.get('core_subjects_avg', 0),
            data.get('project_score', 0),
            data.get('percentage', 0)
        ]
    elif level == 'ITI':
        trade_encoded = model_data['specialization_encoder'].transform([data.get('trade', 'Electrician')])[0]
        features = [
            trade_encoded,
            data.get('practical_score', 0),
            data.get('theory_score', 0),
            data.get('percentage', 0)
        ]
    elif level == 'Bachelors':
        branch_encoded = model_data['specialization_encoder'].transform([data.get('branch', 'CS')])[0]
        features = [
            branch_encoded,
            data.get('cgpa', 0),
            data.get('project_score', 0),
            data.get('internship_rating', 0)
        ]
    else:  # Masters
        specialization_encoded = model_data['specialization_encoder'].transform([data.get('specialization', 'AI/ML')])[0]
        features = [
            specialization_encoded,
            data.get('cgpa', 0),
            data.get('research_score', 0),
            data.get('publication_count', 0)
        ]

    features = np.array([features])
    return model_data['scaler'].transform(features)

@app.route('/api/recommendations', methods=['POST', 'OPTIONS'])
def get_recommendations():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'CORS Preflight successful'}), 200

    try:
        data = request.json
        if 'level' not in data:
            return jsonify({'error': 'Education level is required'}), 400

        level = data['level']
        if level not in models:
            return jsonify({'error': f'Invalid education level: {level}'}), 400

        features = prepare_features(data, level)
        model_data = models[level]
        ml_prediction = model_data['model'].predict_proba(features)[0]
        ml_recommendation = create_ml_recommendation(ml_prediction, model_data['pathway_encoder'], level)

        ai_recommendation = get_ai_recommendation(data)

        return jsonify({
            'ml': ml_recommendation,
            'ai': ai_recommendation
        })
    except Exception as e:
        print(f"Error processing recommendations: {e}")
        return jsonify({'error': str(e)}), 500

def create_ml_recommendation(prediction_probs, pathway_encoder, level):
    pathway_idx = np.argmax(prediction_probs)
    pathway = pathway_encoder.inverse_transform([pathway_idx])[0]
    confidence = float(prediction_probs[pathway_idx] * 100)

    # Level-specific pathway details
    pathway_details = {
        'SSLC': {
            'Science PU': {
                'description': 'Strong foundation in science and mathematics',
                'requirements': ['Good marks in Science and Maths', 'Analytical thinking'],
                'timeframe': '2 years for PU',
                'careers': ['Engineering', 'Medical', 'Research']
            },
            'Commerce PU': {
                'description': 'Aptitude for business and commerce',
                'requirements': ['Good mathematical skills', 'Business interest'],
                'timeframe': '2 years for PU',
                'careers': ['CA', 'Business Management', 'Banking']
            }
        },
        'PU': {
            'Engineering': {
                'description': 'Strong technical and analytical capabilities',
                'requirements': ['Strong in PCM', 'Problem-solving skills'],
                'timeframe': '4 years for BE/BTech',
                'careers': ['Engineer', 'Technical Consultant', 'Product Manager']
            },
            'Medical': {
                'description': 'Excellence in biology and sciences',
                'requirements': ['Strong in PCB', 'Dedication to healthcare'],
                'timeframe': '5.5 years for MBBS',
                'careers': ['Doctor', 'Surgeon', 'Medical Researcher']
            }
        },
        # Add similar details for other levels...
    }

    level_details = pathway_details.get(level, {})
    details = level_details.get(pathway, {
        'description': f'Suitable pathway based on your {level} performance',
        'requirements': ['Good academic performance', 'Relevant coursework'],
        'timeframe': '2-4 years',
        'careers': ['Professional in ' + pathway]
    })

    return {
        'pathway': pathway,
        'confidence': confidence,
        **details
    }

def get_ai_recommendation(data):
    performance_text = ""
    if data.get('percentage'):
        performance_text = f"Percentage: {data['percentage']}%"
    elif data.get('cgpa'):
        performance_text = f"CGPA: {data['cgpa']}"
    else:
        marks = [
            f"Science: {data.get('science_marks')}",
            f"Maths: {data.get('maths_marks')}",
            f"English: {data.get('english_marks')}"
        ]
        performance_text = ", ".join(marks)

    prompt = f"""Given a student's educational background:
    Level: {data['level']}
    {performance_text}
    Specialization (if any): {data.get('specialization', 'None')}
    
    Provide a detailed educational pathway recommendation including:
    1. Recommended course/field
    2. Confidence level (as a percentage)
    3. Brief description of why this path is suitable
    4. Key requirements or prerequisites
    5. Expected timeframe for completion
    6. Potential career paths

    Format the response as JSON with these exact keys:
    {{
        "pathway": "string",
        "confidence": number,
        "description": "string",
        "requirements": ["string"],
        "timeframe": "string",
        "careers": ["string"]
    }}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert educational advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert educational advisor."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({'reply': reply})
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return jsonify({'error': 'Failed to get AI response'}), 500

if __name__ == '__main__':
    app.run(debug=True)
