from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import numpy as np
import pandas as pd
import pickle
import os
import json
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional


load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the ML model (Random Forest)
try:
    with open('model/random_forest_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
except FileNotFoundError:
    print("Warning: ML model file not found. ML recommendations will be simulated.")
    ml_model = None

# Helper functions
def format_recommendation(
    pathway: str,
    confidence: float,
    description: str,
    requirements: List[str],
    timeframe: str,
    careers: List[str]
) -> Dict[str, Any]:
    """Format a recommendation object"""
    return {
        "pathway": pathway,
        "confidence": confidence,
        "description": description,
        "requirements": requirements,
        "timeframe": timeframe,
        "careers": careers
    }

def get_gpt_response(prompt: str, system_message: str = None, max_tokens: int = 500) -> str:
    """Get a response from OpenAI GPT using the updated API"""
    messages = []

    if system_message:
        messages.append({"role": "system", "content": system_message})

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # You can change to gpt-3.5-turbo for cost efficiency
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

def generate_ai_recommendation(education_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate AI-based education pathway recommendation using OpenAI"""
    level = education_data.get("level", "")
    marks = education_data.get("marks", {})
    
    # Create a detailed prompt based on the user's educational data
    prompt = f"""
    I need an educational pathway recommendation for a student with the following profile:
    Education Level: {level}
    """
    
    if level == "SSLC":
        science = marks.get("science_marks", "N/A")
        maths = marks.get("maths_marks", "N/A")
        english = marks.get("english_marks", "N/A")
        prompt += f"Science Marks: {science}\nMaths Marks: {maths}\nEnglish Marks: {english}\n"
    elif level in ["PU", "Diploma", "ITI"]:
        specialization = marks.get("specialization", "N/A")
        percentage = marks.get("percentage", "N/A")
        prompt += f"Specialization: {specialization}\nPercentage: {percentage}%\n"
    elif level in ["Bachelors", "Masters"]:
        specialization = marks.get("specialization", "N/A")
        cgpa = marks.get("cgpa", "N/A")
        prompt += f"Specialization: {specialization}\nCGPA: {cgpa}\n"
    
    prompt += """
    Based on this profile, provide a suitable educational pathway recommendation in the following JSON format:
    {
        "pathway": "Recommended educational pathway",
        "confidence": 95.5, (a percentage between 70 and 99)
        "description": "A detailed description of why this pathway is suitable",
        "requirements": ["requirement1", "requirement2", "requirement3"],
        "timeframe": "Duration or timeframe to complete this pathway",
        "careers": ["career1", "career2", "career3", "career4"]
    }
    
    Please provide only the JSON output without any additional text.
    """
    
    system_message = "You are an AI educational advisor that analyzes student profiles and recommends the most suitable educational pathways."
    
    try:
        response = get_gpt_response(prompt, system_message, max_tokens=800)
        if not response:
            raise ValueError("No response from OpenAI API")
            
        # Extract JSON from response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            recommendation = json.loads(json_str)
            return recommendation
        else:
            raise ValueError("Could not extract valid JSON from GPT response")
    except Exception as e:
        print(f"Error generating AI recommendation: {e}")
        # Fallback recommendation
        return format_recommendation(
            pathway="Higher Education in Science",
            confidence=85.0,
            description="This recommendation is based on your academic profile. Further personalized advice is currently unavailable.",
            requirements=["Bachelor's degree in a relevant field", "Good academic standing"],
            timeframe="3-4 years",
            careers=["Research Scientist", "Data Analyst", "Laboratory Technician"]
        )

def generate_ml_recommendation(education_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate ML-based education pathway recommendation using Random Forest model"""
    level = education_data.get("level", "")
    marks = education_data.get("marks", {})
    
    # Process features based on education level
    features = []
    if level == "SSLC":
        science = marks.get("science_marks", 0)
        maths = marks.get("maths_marks", 0)
        english = marks.get("english_marks", 0)
        features = [science, maths, english]
    elif level in ["PU", "Diploma", "ITI"]:
        specialization = marks.get("specialization", "")
        percentage = marks.get("percentage", 0)
        # Ensure we have 3 features to match the model's expectation
        features = [percentage, 0, 0]  # Padding with zeros
    elif level in ["Bachelors", "Masters"]:
        specialization = marks.get("specialization", "")
        cgpa = marks.get("cgpa", 0)
        # Ensure we have 3 features to match the model's expectation
        features = [cgpa, 0, 0]  # Padding with zeros
    
    # If we have a valid model, use it for prediction
    if ml_model is not None:
        try:
            # Ensure we have exactly 3 features (the number the model expects)
            if len(features) != 3:
                features = features[:3] if len(features) > 3 else features + [0] * (3 - len(features))
                
            # Reshape features for prediction
            features_array = np.array(features).reshape(1, -1)
            # Get prediction (assuming model outputs pathway index)
            pathway_index = ml_model.predict(features_array)[0]
            # Get prediction probability
            probabilities = ml_model.predict_proba(features_array)[0]
            confidence = float(np.max(probabilities) * 100)
            
            # Map index to pathway (this mapping should match your training data)
            pathways = [
                "Computer Science & IT",
                "Engineering",
                "Medicine & Healthcare",
                "Business & Management",
                "Arts & Humanities",
                "Vocational Training"
            ]
            
            pathway = pathways[pathway_index % len(pathways)]
            
            # Generate recommendation details based on pathway
            if pathway == "Computer Science & IT":
                description = "Based on your academic performance, you show strong aptitude for computer science and information technology fields."
                requirements = ["Strong analytical skills", "Bachelor's in Computer Science or related field", "Programming knowledge"]
                timeframe = "4 years for Bachelor's degree"
                careers = ["Software Developer", "Data Scientist", "Systems Analyst", "Network Administrator"]
            elif pathway == "Engineering":
                description = "Your marks indicate you have strong potential for engineering disciplines."
                requirements = ["Strong mathematics foundation", "Bachelor's in Engineering", "Problem-solving skills"]
                timeframe = "4-5 years for Bachelor's degree"
                careers = ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Chemical Engineer"]
            elif pathway == "Medicine & Healthcare":
                description = "Your academic profile suggests you would excel in medicine and healthcare fields."
                requirements = ["Strong science background", "Medical school admission", "Dedication to lengthy study"]
                timeframe = "5-8 years depending on specialization"
                careers = ["Doctor", "Nurse", "Medical Researcher", "Healthcare Administrator"]
            elif pathway == "Business & Management":
                description = "Your profile indicates aptitude for business and management disciplines."
                requirements = ["Bachelor's in Business Administration", "Communication skills", "Analytical thinking"]
                timeframe = "3-4 years for Bachelor's degree"
                careers = ["Business Analyst", "Marketing Manager", "Financial Advisor", "Entrepreneur"]
            elif pathway == "Arts & Humanities":
                description = "Your academic profile suggests you would thrive in arts and humanities fields."
                requirements = ["Bachelor's in relevant humanities field", "Critical thinking", "Communication skills"]
                timeframe = "3-4 years for Bachelor's degree"
                careers = ["Writer", "Teacher", "Journalist", "Public Relations Specialist"]
            else:  # Vocational Training
                description = "Based on your profile, practical vocational training could be a great fit for your skills."
                requirements = ["High school diploma", "Specific vocational training", "Hands-on skills"]
                timeframe = "6 months - 2 years depending on program"
                careers = ["Electrician", "Plumber", "Automotive Technician", "Construction Manager"]
            
            return format_recommendation(
                pathway=pathway,
                confidence=confidence,
                description=description,
                requirements=requirements,
                timeframe=timeframe,
                careers=careers
            )
        except Exception as e:
            print(f"Error using ML model: {e}")
    
    # Fallback or simulation if model fails or doesn't exist
    print("Using simulated ML recommendation")
    
    # Simple rule-based recommendation based on education level and marks
    pathway = "General Higher Education"
    confidence = 78.5
    description = "Based on your academic profile, continuing with higher education is recommended."
    requirements = ["Complete current education level", "Apply to relevant institutions"]
    timeframe = "2-4 years"
    careers = ["Professional", "Researcher", "Educator", "Analyst"]
    
    if level == "SSLC":
        science = marks.get("science_marks", 0)
        maths = marks.get("maths_marks", 0)
        
        if science > 80 and maths > 80:
            pathway = "Science Stream in PU"
            confidence = 88.5
            description = "Your strong performance in science and mathematics suggests you would excel in science streams."
            careers = ["Engineer", "Doctor", "Scientist", "IT Professional"]
        elif maths > 80:
            pathway = "Commerce with Mathematics"
            confidence = 85.2
            description = "Your strong mathematics skills suggest aptitude for commerce with mathematics."
            careers = ["Accountant", "Financial Analyst", "Economist", "Business Analyst"]
    
    elif level == "PU":
        percentage = marks.get("percentage", 0)
        specialization = marks.get("specialization", "").lower()
        
        if percentage > 85 and "science" in specialization:
            pathway = "Engineering or Medical Degree"
            confidence = 90.1
            description = "Your excellent performance in science stream indicates strong potential for engineering or medical fields."
            careers = ["Engineer", "Doctor", "Research Scientist", "Pharmacist"]
        elif percentage > 80 and "commerce" in specialization:
            pathway = "Bachelor's in Commerce or Business"
            confidence = 87.3
            description = "Your strong commerce background suggests you would excel in business-related higher education."
            careers = ["Chartered Accountant", "Business Manager", "Financial Planner", "Marketing Executive"]
    
    return format_recommendation(
        pathway=pathway,
        confidence=confidence,
        description=description,
        requirements=requirements,
        timeframe=timeframe,
        careers=careers
    )

# API Routes
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Chatbot API endpoint"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    system_message = """
    You are an educational advisor chatbot for the Educational Pathfinder platform. 
    Your role is to provide helpful, accurate advice about educational pathways, career options,
    and academic decisions. Be supportive, encouraging, and informative.
    Keep your answers concise but comprehensive, focusing on providing practical advice.
    """
    
    response = get_gpt_response(message, system_message)
    
    if response:
        return jsonify({"reply": response})
    else:
        return jsonify({"error": "Failed to generate response"}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Combined recommendations API endpoint"""
    data = request.json
    
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400
    
    # Generate recommendations using both methods
    ai_recommendation = generate_ai_recommendation(data)
    ml_recommendation = generate_ml_recommendation(data)
    
    return jsonify({
        "ai": ai_recommendation,
        "ml": ml_recommendation
    })
@app.route('/api/skill-gap', methods=['POST'])
def skill_gap_analysis():
    """Skill Gap Analysis API"""
    data = request.json
    level = data.get('level', '')
    skills = data.get('skills', '').split(', ')
    career = data.get('career', '')

    # Sample AI-based skill analysis using OpenAI API
    prompt = f"""
    Analyze the skill gap for a person with education level '{level}', current skills '{', '.join(skills)}', and a desired career '{career}'.
    Identify missing skills and recommend learning resources.
    Provide response in JSON format:
    {{
        "gaps": ["missing_skill1", "missing_skill2"],
        "recommendations": ["resource1", "resource2"]
    }}
    """
    
    system_message = "You are an AI assistant that identifies skill gaps and provides career development recommendations."
    response = get_gpt_response(prompt, system_message)

    try:
        result = json.loads(response)
    except:
        result = {"gaps": ["Unknown"], "recommendations": ["Try online courses"]}

    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Educational Pathfinder API"})

# Run the app
if __name__ == '__main__':
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # If we don't have a model file, create a simple dummy model for demonstration
    if not os.path.exists('model/random_forest_model.pkl'):
        try:
            from sklearn.ensemble import RandomForestClassifier
            dummy_model = RandomForestClassifier(n_estimators=10, random_state=42)
            # Train on dummy data - always use 3 features for consistency
            X = np.random.rand(100, 3)  # Features: primary_score, secondary_score, tertiary_score
            y = np.random.randint(0, 6, 100)  # 6 different pathway classes
            dummy_model.fit(X, y)
            # Save model
            with open('model/random_forest_model.pkl', 'wb') as f:
                pickle.dump(dummy_model, f)
            print("Created dummy ML model for demonstration purposes.")
            ml_model = dummy_model
        except Exception as e:
            print(f"Error creating dummy model: {e}")
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)