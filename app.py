from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_very_secret_key'  # Important for session management

# List of valid numbers (excluding 40, 84, 89)
valid_numbers = [num for num in range(34, 98) if num not in (40, 84, 89)]

# AI-related questions
questions_data = [
    {
        "question": "What does 'AI' stand for?",
        "options": ["Automated Interface", "Artificial Intelligence", "Advanced Integration", "Algorithmic Input"],
        "answer": "Artificial Intelligence"
    },
    {
        "question": "Which of these is a subfield of AI?",
        "options": ["Machine Learning", "Quantum Computing", "Cloud Storage", "Web Development"],
        "answer": "Machine Learning"
    },
    {
        "question": "What is the main goal of AI?",
        "options": ["Store data", "Simulate human intelligence", "Design websites", "Create databases"],
        "answer": "Simulate human intelligence"
    },
    {
        "question": "Which algorithm is commonly used in AI for classification?",
        "options": ["Linear Regression", "K-Nearest Neighbors", "Bubble Sort", "Quick Sort"],
        "answer": "K-Nearest Neighbors"
    },
    {
        "question": "Which language is widely used in AI development?",
        "options": ["Python", "HTML", "CSS", "PHP"],
        "answer": "Python"
    },
    {
        "question": "What does NLP stand for in AI?",
        "options": ["Neural Learning Protocol", "Natural Language Processing", "Numeric Logical Pattern", "Node Link Prediction"],
        "answer": "Natural Language Processing"
    },
    {
        "question": "Which of these is a type of neural network?",
        "options": ["CNN", "GPS", "RAM", "CPU"],
        "answer": "CNN"
    },
    {
        "question": "What is overfitting in machine learning?",
        "options": ["Model works well on all data", "Model memorizes training data", "Data is too simple", "Training never ends"],
        "answer": "Model memorizes training data"
    },
    {
        "question": "Which is an example of AI in daily life?",
        "options": ["Google Maps", "Smart Assistants", "Weather Forecast", "All of these"],
        "answer": "All of these"
    },
    {
        "question": "What is the Turing Test used for?",
        "options": ["Test processor speed", "Test AI’s ability to mimic humans", "Test storage capacity", "Test internet speed"],
        "answer": "Test AI’s ability to mimic humans"
    }
]

@app.route('/')
def index():
    if 'quiz_started' not in session:
        session['quiz_started'] = False
        session['feedback'] = ""
        session['reg_number'] = ""

    return render_template('index.html',
                           quiz_started=session['quiz_started'],
                           feedback=session.get('feedback', ""),
                           reg_number=session.get('reg_number', ""))

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    session['quiz_started'] = True
    session['available_questions'] = questions_data.copy()
    session.pop('current_question', None) # Clear previous question
    session.pop('feedback', None)
    session.pop('reg_number', None)
    return redirect(url_for('index'))

@app.route('/spin_wheel', methods=['POST'])
def spin_wheel():
    if not session.get('quiz_started'):
        return redirect(url_for('index'))

    if not session.get('available_questions'):
        session['available_questions'] = questions_data.copy() # Reset if empty
        session['feedback'] = "All questions asked. Resetting the quiz. Spin again!"
        return redirect(url_for('index'))

    random_number = random.choice(valid_numbers)
    current_question = random.choice(session['available_questions'])
    session['available_questions'].remove(current_question)

    session['current_question'] = current_question
    session['reg_number'] = random_number
    session['timer_seconds'] = 15 # Initial timer duration
    session.pop('feedback', None) # Clear previous feedback

    return redirect(url_for('show_quiz'))

@app.route('/quiz')
def show_quiz():
    if not session.get('quiz_started') or 'current_question' not in session:
        return redirect(url_for('index'))

    return render_template('quiz.html',
                           question_data=session['current_question'],
                           reg_number=session['reg_number'],
                           timer_seconds=session['timer_seconds'])

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if not session.get('quiz_started') or 'current_question' not in session:
        return redirect(url_for('index'))

    selected_option = request.form.get('option')
    correct_answer = session['current_question']['answer']

    if selected_option == correct_answer:
        session['feedback'] = "✅ Correct!"
    elif selected_option is None and request.form.get('time_up'): # Check if time_up signal is sent
        session['feedback'] = f"⏰ Time's up! Answer: {correct_answer}"
    else:
        session['feedback'] = f"❌ Wrong! Answer: {correct_answer}"

    session.pop('current_question', None) # Remove current question to prompt for new spin
    return redirect(url_for('index'))

@app.route('/test_connection')
def test_connection():
    return "Backend is connected to the frontend!"


if __name__ == '__main__':
    app.run(debug=True)