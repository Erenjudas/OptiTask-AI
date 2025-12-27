from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initial weights
weights = {
    "importance": 3.0,
    "difficulty": 2.0,
    "deadline_factor": 1.0
}

@app.route('/score', methods=['POST'])
def calculate_score():
    data = request.json
    importance = data.get('importance', 0)
    difficulty = data.get('difficulty', 0)
    deadline = data.get('deadline', 0)
    
    # score = importance*3 + difficulty*2 + (10 - deadline)
    score = (importance * weights["importance"]) + \
            (difficulty * weights["difficulty"]) + \
            (10 - deadline) * weights["deadline_factor"]
    
    recommendation = "📝 Can Wait"
    if score >= 15:
        recommendation = "🔥 Do Now"
    elif score >= 10:
        recommendation = "⏳ Schedule Soon"
        
    return jsonify({
        "priorityScore": round(score, 2),
        "recommendation": recommendation
    })

@app.route('/train', methods=['POST'])
def train_model():
    global weights
    data = request.json
    history = data.get('history', [])
    
    # Simple adaptive logic: if many tasks are completed on time, 
    # maybe importance should weigh more. If many are delayed, 
    # maybe deadline should weigh more.
    # This is a placeholder for a more complex ML model.
    
    completed_count = sum(1 for h in history if h['Action'] == 'Completed')
    delayed_count = sum(1 for h in history if h['Action'] == 'Delayed')
    
    if completed_count > delayed_count:
        weights["importance"] += 0.1
    elif delayed_count > completed_count:
        weights["deadline_factor"] += 0.1
        
    return jsonify({
        "status": "success",
        "new_weights": weights
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "Online",
        "model_loaded": True,
        "weights": weights
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
