from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Base path to the marks files directory
marks_base_path = 'C:\\rtp\\prac-2\\'

# Paths to the Excel files
student_credentials_path = 'C:\\rtp\\prac-2\\student_credentials.xlsx'
teacher_credentials_path = 'C:\\rtp\\prac-2\\teacher_credentials.xlsx'

@app.route('/')
def begin():
    return render_template('begin.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login/student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Load student credentials
        credentials_df = pd.read_excel(student_credentials_path, engine='openpyxl')
        student = credentials_df[(credentials_df['Username'] == username) & (credentials_df['Password'] == password)]
        
        if not student.empty:
            student_details = student.iloc[0].to_dict()
            return redirect(url_for('student_dashboard', **student_details))
        else:
            return 'Invalid credentials'
    return render_template('student_login.html')

@app.route('/login/teacher', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Load teacher credentials
        credentials_df = pd.read_excel(teacher_credentials_path, engine='openpyxl')
        teacher = credentials_df[(credentials_df['Username'] == username) & (credentials_df['Password'] == password)]
        
        if not teacher.empty:
            teacher_details = teacher.iloc[0].to_dict()
            return redirect(url_for('teacher_dashboard', **teacher_details))
        else:
            return 'Invalid credentials'
    return render_template('teacher_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    student_details = request.args.to_dict()
    return render_template('student_dashboard.html', student_details=student_details)

@app.route('/student_dashboard/marks')
def student_marks():
    username = request.args.get('Username')
    exam = request.args.get('exam')
    
    # Determine the path to the marks file based on the exam
    marks_file_path = os.path.join(marks_base_path, f"{exam}marks.xlsx")
    
    try:
        marks_df = pd.read_excel(marks_file_path, engine='openpyxl')
        student_marks = marks_df[marks_df['Username'] == username]
        
        if not student_marks.empty:
            subjects = ['Telugu', 'Hindi', 'English', 'Maths', 'Science', 'Social']
            marks = [int(student_marks[subject].values[0]) for subject in subjects]

            marks_data = {
                'Subject': subjects,
                'Marks': marks
            }
        else:
            marks_data = {
                'Subject': [],
                'Marks': []
            }
    except FileNotFoundError:
        marks_data = {
            'Subject': [],
            'Marks': []
        }
    
    return render_template('student_marks.html', marks_data=marks_data)

@app.route('/teacher_dashboard')
def teacher_dashboard():
    teacher_details = request.args.to_dict()
    return render_template('teacher_dashboard.html', teacher_details=teacher_details)

if __name__ == '__main__':
    app.run(debug=True)
