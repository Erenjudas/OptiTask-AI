from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
import requests
import json

app = Flask(__name__)
CORS(app)

# SQL Server Connection
conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=.\SQLEXPRESS;'
    r'DATABASE=OptiTaskDB;'
    r'Trusted_Connection=yes;'
)

def get_db_connection():
    return pyodbc.connect(conn_str)

ML_ENGINE_URL = "http://localhost:5000"

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    name = data.get('name')
    deadline = data.get('deadline')
    difficulty = data.get('difficulty')
    importance = data.get('importance')
    
    # 1. Call ML Engine for scoring
    try:
        ml_response = requests.post(f"{ML_ENGINE_URL}/score", json={
            "deadline": deadline,
            "difficulty": difficulty,
            "importance": importance
        })
        ml_data = ml_response.json()
        priority_score = ml_data.get('priorityScore')
        recommendation = ml_data.get('recommendation')
    except Exception as e:
        print(f"ML Engine Error: {e}")
        priority_score = 0
        recommendation = "Error"

    # 2. Store in SQL Server
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Tasks (Name, Deadline, Difficulty, Importance, PriorityScore, Recommendation, Status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    """, (name, deadline, difficulty, importance, priority_score, recommendation))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "priorityScore": priority_score, "recommendation": recommendation})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tasks ORDER BY PriorityScore DESC")
    rows = cursor.fetchall()
    
    tasks = []
    for row in rows:
        tasks.append({
            "id": row.TaskID,
            "name": row.Name,
            "deadline": row.Deadline,
            "difficulty": row.Difficulty,
            "importance": row.Importance,
            "priorityScore": row.PriorityScore,
            "recommendation": row.Recommendation,
            "status": row.Status
        })
    conn.close()
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>/feedback', methods=['POST'])
def task_feedback(task_id):
    data = request.json
    action = data.get('action') # 'Completed' or 'Delayed'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update task status
    cursor.execute("UPDATE Tasks SET Status = ? WHERE TaskID = ?", (action, task_id))
    
    # Add to history
    cursor.execute("INSERT INTO TaskHistory (TaskID, Action) VALUES (?, ?)", (task_id, action))
    conn.commit()
    
    # Trigger ML training loop
    try:
        cursor.execute("SELECT Action FROM TaskHistory")
        history_rows = cursor.fetchall()
        history = [{"Action": row.Action} for row in history_rows]
        requests.post(f"{ML_ENGINE_URL}/train", json={"history": history})
    except Exception as e:
        print(f"ML Training Error: {e}")
        
    conn.close()
    return jsonify({"status": "success"})

@app.route('/system/health', methods=['GET'])
def system_health():
    try:
        conn = get_db_connection()
        conn.close()
        db_status = "Connected"
    except:
        db_status = "Disconnected"
        
    try:
        ml_health = requests.get(f"{ML_ENGINE_URL}/health").json()
        ml_status = ml_health.get("status", "Offline")
    except:
        ml_status = "Offline"
        
    return jsonify({
        "database": db_status,
        "ml_engine": ml_status,
        "backend": "Online",
        "uptime": "99.9%",
        "agent_version": "v2.0.26"
    })

if __name__ == '__main__':
    app.run(port=8000, debug=True)
