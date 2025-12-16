from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'simple_attendance_key_123'

# ===== SIMPLE CORS FIX =====
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Database file
DB_FILE = 'database.json'

def load_database():
    """Load database from JSON file"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    else:
        # Initialize with default structure
        default_db = {
            "users": {
                "admin": [
                    {
                        "user_id": "ADMIN_001",
                        "name": "System Admin",
                        "password": "admin123"
                    }
                ],
                "teachers": [
                    {
                        "user_id": "TCH_001",
                        "name": "John Teacher",
                        "email": "john.teacher@school.edu",
                        "password": "teacher123",
                        "join_date": "2023-08-15"
                    }
                ],
                "students": [
                    {
                        "user_id": "STU_001",
                        "name": "Alice Student",
                        "password": "student123",
                        "department": "Class 10A"
                    }
                ]
            },
            "teacher_assignments": {
                "TCH_001": {
                    "name": "John Teacher",
                    "email": "john.teacher@school.edu",
                    "joined_date": "2023-08-15",
                    "password": "teacher123",
                    "subjects": {
                        "Mathematics": ["Class 10A", "Class 11A"],
                        "Science": ["Class 10A"]
                    }
                }
            },
            "student_data": {
                "Class 10A": [
                    {
                        "id": "STU_001",
                        "name": "Alice Student",
                        "department": "Class 10A",
                        "password": "student123"
                    }
                ]
            },
            "attendance_records": {
                "STU_001": [
                    {
                        "date": "2024-01-15",
                        "subject": "Mathematics",
                        "status": "present",
                        "teacher_id": "TCH_001"
                    },
                    {
                        "date": "2024-01-15",
                        "subject": "Science",
                        "status": "present",
                        "teacher_id": "TCH_001"
                    }
                ]
            },
            "student_timetables": {
                "STU_001": {
                    "monday": [
                        {
                            "time": "9:00-10:00",
                            "subject": "Mathematics",
                            "teacher": "TCH_001"
                        },
                        {
                            "time": "10:00-11:00",
                            "subject": "Science",
                            "teacher": "TCH_001"
                        }
                    ],
                    "tuesday": [
                        {
                            "time": "9:00-10:00",
                            "subject": "Mathematics",
                            "teacher": "TCH_001"
                        }
                    ],
                    "wednesday": [
                        {
                            "time": "9:00-10:00",
                            "subject": "Science",
                            "teacher": "TCH_001"
                        }
                    ],
                    "thursday": [
                        {
                            "time": "9:00-10:00",
                            "subject": "Mathematics",
                            "teacher": "TCH_001"
                        }
                    ],
                    "friday": [
                        {
                            "time": "9:00-10:00",
                            "subject": "Science",
                            "teacher": "TCH_001"
                        }
                    ],
                    "saturday": []
                }
            },
            "timetable_edit_mode": {},
            "available_departments": ["Class 10A", "Class 11A", "Class 12A", "Class 10B", "Class 11B"],
            "available_subjects": ["Mathematics", "Science", "English", "History", "Physics", "Chemistry", "Biology", "Computer Science"]
        }
        save_database(default_db)
        return default_db

def save_database(data):
    """Save database to JSON file"""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ===== ADD CORS HEADERS MIDDLEWARE =====
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# ===== AUTHENTICATION ENDPOINTS =====
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    role = data.get('role')
    
    print(f"Login attempt: {user_id}, role: {role}")
    
    db = load_database()
    
    # Find user based on role
    if role == 'admin':
        users = db['users']['admin']
    elif role == 'teacher':
        users = db['users']['teachers']
    elif role == 'student':
        users = db['users']['students']
    else:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400
    
    # Find user
    user = None
    for u in users:
        if u['user_id'] == user_id and u['password'] == password:
            user = u
            break
    
    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    # Create session
    session['user_id'] = user_id
    session['role'] = role
    session['name'] = user['name']
    
    return jsonify({
        'success': True,
        'user': {
            'user_id': user_id,
            'name': user['name'],
            'role': role,
            'email': user.get('email', ''),
            'department': user.get('department', '')
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})

# ===== ADMIN ENDPOINTS =====
@app.route('/api/admin/add-teacher', methods=['POST'])
def add_teacher():
    data = request.json
    db = load_database()
    
    # Check if teacher ID already exists
    for teacher in db['users']['teachers']:
        if teacher['user_id'] == data['teacher_id']:
            return jsonify({'success': False, 'message': 'Teacher ID already exists'}), 400
    
    # Add to users
    new_teacher = {
        'user_id': data['teacher_id'],
        'name': data['name'],
        'email': data['email'],
        'password': data['password'],
        'join_date': data['join_date']
    }
    db['users']['teachers'].append(new_teacher)
    
    # Add to teacher assignments
    db['teacher_assignments'][data['teacher_id']] = {
        'name': data['name'],
        'email': data['email'],
        'join_date': data['join_date'],
        'password': data['password'],
        'subjects': data['subjects']
    }
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Teacher added successfully'})

@app.route('/api/admin/teachers', methods=['GET'])
def get_all_teachers():
    db = load_database()
    teachers = []
    
    for teacher in db['users']['teachers']:
        teacher_id = teacher['user_id']
        assignment = db['teacher_assignments'].get(teacher_id, {})
        teachers.append({
            'user_id': teacher_id,
            'name': teacher['name'],
            'email': teacher['email'],
            'password': teacher.get('password', ''),
            'join_date': teacher['join_date'],
            'subjects': assignment.get('subjects', {})
        })
    
    # Sort teachers by ID in numerical order (TCH_001, TCH_002, etc.)
    teachers.sort(key=lambda x: int(x['user_id'].replace('TCH_', '')) if x['user_id'].startswith('TCH_') else float('inf'))
    
    return jsonify({'success': True, 'teachers': teachers})

@app.route('/api/admin/teacher/<teacher_id>', methods=['GET'])
def get_teacher_details(teacher_id):
    db = load_database()
    
    # Find teacher in users
    teacher = None
    for t in db['users']['teachers']:
        if t['user_id'] == teacher_id:
            teacher = t
            break
    
    if not teacher:
        return jsonify({'success': False, 'message': 'Teacher not found'}), 404
    
    # Get assignment details
    assignment = db['teacher_assignments'].get(teacher_id, {})
    
    teacher_details = {
        'user_id': teacher_id,
        'name': teacher['name'],
        'email': teacher['email'],
        'password': teacher.get('password', ''),
        'join_date': teacher['join_date'],
        'subjects': assignment.get('subjects', {})
    }
    
    return jsonify({'success': True, 'teacher': teacher_details})

@app.route('/api/admin/teacher/<teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    data = request.json
    db = load_database()
    
    # Update in users
    for teacher in db['users']['teachers']:
        if teacher['user_id'] == teacher_id:
            teacher['name'] = data['name']
            teacher['email'] = data['email']
            teacher['password'] = data['password']
            teacher['join_date'] = data['join_date']
            break
    
    # Update in teacher assignments
    if teacher_id in db['teacher_assignments']:
        db['teacher_assignments'][teacher_id]['name'] = data['name']
        db['teacher_assignments'][teacher_id]['email'] = data['email']
        db['teacher_assignments'][teacher_id]['password'] = data['password']
        db['teacher_assignments'][teacher_id]['join_date'] = data['join_date']
        db['teacher_assignments'][teacher_id]['subjects'] = data['subjects']
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Teacher updated successfully'})

@app.route('/api/admin/teacher/<teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    db = load_database()
    
    # Remove from users
    db['users']['teachers'] = [t for t in db['users']['teachers'] if t['user_id'] != teacher_id]
    
    # Remove from teacher assignments
    if teacher_id in db['teacher_assignments']:
        del db['teacher_assignments'][teacher_id]
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Teacher deleted successfully'})

@app.route('/api/admin/available-data', methods=['GET'])
def get_available_data():
    db = load_database()
    
    # Get all departments from student_data
    all_departments = list(db['student_data'].keys())
    # Also include predefined departments
    all_departments = list(set(all_departments + db.get('available_departments', [])))
    
    # Get all subjects from teacher assignments
    all_subjects = set()
    for assignment in db['teacher_assignments'].values():
        all_subjects.update(assignment.get('subjects', {}).keys())
    # Also include predefined subjects
    all_subjects = list(set(all_subjects) | set(db.get('available_subjects', [])))
    
    return jsonify({
        'success': True,
        'departments': all_departments,
        'subjects': list(all_subjects)
    })

# ===== TEACHER ENDPOINTS =====
@app.route('/api/teacher/add-student', methods=['POST'])
def add_student():
    data = request.json
    db = load_database()
    
    # Check if student ID already exists
    for student in db['users']['students']:
        if student['user_id'] == data['student_id']:
            return jsonify({'success': False, 'message': 'Student ID already exists'}), 400
    
    # Add to users
    new_student = {
        'user_id': data['student_id'],
        'name': data['name'],
        'password': data['password'],
        'department': data['department']
    }
    db['users']['students'].append(new_student)
    
    # Add to student_data
    if data['department'] not in db['student_data']:
        db['student_data'][data['department']] = []
    
    db['student_data'][data['department']].append({
        'id': data['student_id'],
        'name': data['name'],
        'department': data['department'],
        'password': data['password']
    })
    
    # Initialize empty attendance records
    if data['student_id'] not in db['attendance_records']:
        db['attendance_records'][data['student_id']] = []
    
    # Initialize empty timetable
    if data['student_id'] not in db['student_timetables']:
        db['student_timetables'][data['student_id']] = {
            'monday': [], 'tuesday': [], 'wednesday': [],
            'thursday': [], 'friday': [], 'saturday': []
        }
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Student added successfully'})

@app.route('/api/teacher/mark-attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    teacher_id = session.get('user_id', 'TCH_001')  # Use logged in teacher
    date = data['date']
    department = data['department']
    subject = data['subject']
    attendance_data = data['attendance_data']
    
    db = load_database()
    
    # Check if teacher is assigned to this subject and department
    teacher_assignment = db['teacher_assignments'].get(teacher_id, {})
    if subject not in teacher_assignment.get('subjects', {}):
        return jsonify({'success': False, 'message': f'You are not assigned to teach {subject}'}), 403
    
    if department not in teacher_assignment.get('subjects', {}).get(subject, []):
        return jsonify({'success': False, 'message': f'You are not assigned to teach {subject} in {department}'}), 403
    
    # Mark attendance for each student
    for student_id, status in attendance_data.items():
        if student_id not in db['attendance_records']:
            db['attendance_records'][student_id] = []
        
        # Check if attendance already exists for this date and subject
        existing_index = -1
        for i, record in enumerate(db['attendance_records'][student_id]):
            if record['date'] == date and record['subject'] == subject and record['teacher_id'] == teacher_id:
                existing_index = i
                break
        
        new_record = {
            'date': date,
            'subject': subject,
            'status': status,
            'teacher_id': teacher_id,
            'department': department
        }
        
        if existing_index >= 0:
            # Update existing record
            db['attendance_records'][student_id][existing_index] = new_record
        else:
            # Add new record
            db['attendance_records'][student_id].append(new_record)
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Attendance marked successfully'})

@app.route('/api/teacher/students', methods=['GET'])
def get_teacher_students():
    db = load_database()
    
    # Get current teacher's departments
    teacher_id = session.get('user_id', 'TCH_001')
    teacher_assignment = db['teacher_assignments'].get(teacher_id, {})
    subjects = teacher_assignment.get('subjects', {})
    
    # Get all departments assigned to this teacher
    teacher_departments = set()
    for dept_list in subjects.values():
        teacher_departments.update(dept_list)
    
    # Get all students from teacher's departments
    all_students = []
    for department, students in db['student_data'].items():
        if department in teacher_departments:
            all_students.extend(students)
    
    # Calculate attendance percentage for each student
    for student in all_students:
        student_id = student['id']
        attendance_records = db['attendance_records'].get(student_id, [])
        
        if attendance_records:
            present_count = len([r for r in attendance_records if r['status'] == 'present'])
            total_count = len(attendance_records)
            student['attendance_percentage'] = round((present_count / total_count) * 100) if total_count > 0 else 0
            student['attendance_percentage_data'] = {
                'present': present_count,
                'total': total_count
            }
        else:
            student['attendance_percentage'] = 0
            student['attendance_percentage_data'] = {
                'present': 0,
                'total': 0
            }
        
        # Add subject information
        if attendance_records:
            # Get most recent subject
            student['subject'] = attendance_records[-1]['subject'] if attendance_records else 'All Subjects'
        else:
            student['subject'] = 'All Subjects'
    
    return jsonify({'success': True, 'students': all_students})

@app.route('/api/teacher/student-details', methods=['GET'])
def get_teacher_student_details():
    db = load_database()
    
    # Get current teacher
    teacher_id = session.get('user_id', 'TCH_001')
    teacher_assignment = db['teacher_assignments'].get(teacher_id, {})
    teacher_subjects = teacher_assignment.get('subjects', {})
    
    # Get all departments assigned to this teacher
    teacher_departments = set()
    for dept_list in teacher_subjects.values():
        teacher_departments.update(dept_list)
    
    # Get all students from teacher's departments
    student_details = {}
    
    for department, students in db['student_data'].items():
        if department in teacher_departments:
            for student in students:
                student_id = student['id']
                attendance_records = db['attendance_records'].get(student_id, [])
                
                # Filter attendance records for this teacher only
                teacher_records = [r for r in attendance_records if r['teacher_id'] == teacher_id]
                
                # Calculate subject-wise attendance for this teacher
                subject_attendance = {}
                for record in teacher_records:
                    subject = record['subject']
                    if subject not in subject_attendance:
                        subject_attendance[subject] = {'present': 0, 'absent': 0, 'total': 0}
                    
                    subject_attendance[subject]['total'] += 1
                    if record['status'] == 'present':
                        subject_attendance[subject]['present'] += 1
                    else:
                        subject_attendance[subject]['absent'] += 1
                
                # Calculate overall attendance by this teacher
                total_present = sum([s['present'] for s in subject_attendance.values()])
                total_records = sum([s['total'] for s in subject_attendance.values()])
                overall_percentage = round((total_present / total_records * 100)) if total_records > 0 else 0
                
                student_details[student_id] = {
                    'name': student['name'],
                    'department': student['department'],
                    'password': student['password'],
                    'subject_attendance': subject_attendance,
                    'overall_percentage': overall_percentage,
                    'total_records': total_records,
                    'total_present': total_present
                }
    
    return jsonify({
        'success': True,
        'student_details': student_details
    })

@app.route('/api/teacher/subjects', methods=['GET'])
def get_teacher_subjects():
    db = load_database()
    
    teacher_id = session.get('user_id', 'TCH_001')
    teacher_assignment = db['teacher_assignments'].get(teacher_id, {})
    subjects = teacher_assignment.get('subjects', {})
    
    # Get all unique departments
    all_departments = set()
    for dept_list in subjects.values():
        all_departments.update(dept_list)
    
    return jsonify({
        'success': True,
        'subjects': subjects,
        'departments': list(all_departments)
    })

@app.route('/api/teacher/view-attendance', methods=['GET'])
def get_teacher_view_attendance():
    db = load_database()
    
    # Get all attendance records for students in teacher's departments
    teacher_id = session.get('user_id', 'TCH_001')
    teacher_assignment = db['teacher_assignments'].get(teacher_id, {})
    subjects = teacher_assignment.get('subjects', {})
    
    # Get all departments assigned to this teacher
    teacher_departments = set()
    for dept_list in subjects.values():
        teacher_departments.update(dept_list)
    
    # Get all students from teacher's departments
    all_students = []
    for department in teacher_departments:
        if department in db['student_data']:
            all_students.extend(db['student_data'][department])
    
    # Get attendance records for all these students
    attendance_data = {}
    for student in all_students:
        student_id = student['id']
        student_records = db['attendance_records'].get(student_id, [])
        
        # Filter records for this teacher's subjects
        filtered_records = []
        for record in student_records:
            # Check if this subject is taught by this teacher
            record_subject = record.get('subject', '')
            if record_subject in subjects:
                filtered_records.append(record)
        
        # Sort records by date (newest first)
        filtered_records.sort(key=lambda x: x['date'], reverse=True)
        
        if filtered_records:
            attendance_data[student_id] = {
                'name': student['name'],
                'department': student['department'],
                'attendance_records': filtered_records
            }
    
    return jsonify({
        'success': True,
        'attendance_data': attendance_data
    })

@app.route('/api/teacher/available-departments', methods=['GET'])
def get_available_departments():
    db = load_database()
    
    # Get all departments from the database
    all_departments = list(db['student_data'].keys())
    # Also include predefined departments
    all_departments = list(set(all_departments + db.get('available_departments', [])))
    
    return jsonify({
        'success': True,
        'departments': all_departments
    })

@app.route('/api/teacher/update-student/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    db = load_database()
    
    # Update in users
    for student in db['users']['students']:
        if student['user_id'] == student_id:
            student['name'] = data['name']
            student['password'] = data['password']
            student['department'] = data['department']
            break
    
    # Update in student_data
    # First remove from old department
    old_department = None
    for department, students in db['student_data'].items():
        for i, s in enumerate(students):
            if s['id'] == student_id:
                old_department = department
                db['student_data'][department].pop(i)
                break
        if old_department:
            break
    
    # Add to new department
    new_department = data['department']
    if new_department not in db['student_data']:
        db['student_data'][new_department] = []
    
    db['student_data'][new_department].append({
        'id': student_id,
        'name': data['name'],
        'department': new_department,
        'password': data['password']
    })
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Student updated successfully'})

@app.route('/api/teacher/delete-student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    db = load_database()
    
    # Remove from users
    db['users']['students'] = [s for s in db['users']['students'] if s['user_id'] != student_id]
    
    # Remove from student_data
    for department, students in db['student_data'].items():
        db['student_data'][department] = [s for s in students if s['id'] != student_id]
    
    # Remove from attendance_records
    if student_id in db['attendance_records']:
        del db['attendance_records'][student_id]
    
    # Remove from student_timetables
    if student_id in db['student_timetables']:
        del db['student_timetables'][student_id]
    
    # Remove from timetable_edit_mode
    if student_id in db['timetable_edit_mode']:
        del db['timetable_edit_mode'][student_id]
    
    save_database(db)
    return jsonify({'success': True, 'message': 'Student deleted successfully'})

# ===== STUDENT ENDPOINTS =====
@app.route('/api/student/attendance', methods=['GET'])
def get_student_attendance():
    student_id = session.get('user_id', 'STU_001')
    db = load_database()
    
    attendance_records = db['attendance_records'].get(student_id, [])
    
    # Sort attendance records by date (newest first)
    attendance_records.sort(key=lambda x: x['date'], reverse=True)
    
    # Get teacher names
    for record in attendance_records:
        teacher_id = record['teacher_id']
        if teacher_id in db['teacher_assignments']:
            record['teacher_name'] = db['teacher_assignments'][teacher_id]['name']
        else:
            record['teacher_name'] = teacher_id
    
    # Calculate statistics
    present_count = len([r for r in attendance_records if r['status'] == 'present'])
    total_count = len(attendance_records)
    percentage = round((present_count / total_count * 100)) if total_count > 0 else 0
    
    return jsonify({
        'success': True,
        'attendance': attendance_records,
        'statistics': {
            'present': present_count,
            'total': total_count,
            'percentage': percentage
        }
    })

@app.route('/api/student/subject-attendance', methods=['GET'])
def get_student_subject_attendance():
    student_id = session.get('user_id', 'STU_001')
    db = load_database()
    
    attendance_records = db['attendance_records'].get(student_id, [])
    
    # Group by subject
    subject_stats = {}
    for record in attendance_records:
        subject = record['subject']
        if subject not in subject_stats:
            subject_stats[subject] = {'present': 0, 'absent': 0, 'total': 0}
        
        subject_stats[subject]['total'] += 1
        if record['status'] == 'present':
            subject_stats[subject]['present'] += 1
        else:
            subject_stats[subject]['absent'] += 1
    
    # Calculate percentages and format response
    result = []
    total_present = 0
    total_records = 0
    
    for subject, stats in subject_stats.items():
        percentage = round((stats['present'] / stats['total'] * 100)) if stats['total'] > 0 else 0
        result.append({
            'subject': subject,
            'present': stats['present'],
            'absent': stats['absent'],
            'total': stats['total'],
            'percentage': percentage
        })
        total_present += stats['present']
        total_records += stats['total']
    
    # Calculate overall percentage
    overall_percentage = round((total_present / total_records * 100)) if total_records > 0 else 0
    
    return jsonify({
        'success': True,
        'subject_stats': result,
        'overall_percentage': overall_percentage
    })

# ===== GENERAL ENDPOINTS =====
@app.route('/api/system/stats', methods=['GET'])
def get_system_stats():
    db = load_database()
    
    teacher_count = len(db['users']['teachers'])
    student_count = len(db['users']['students'])
    
    # Count total subjects assigned
    total_subjects = 0
    total_departments = 0
    for assignment in db['teacher_assignments'].values():
        total_subjects += len(assignment.get('subjects', {}))
        for dept_list in assignment.get('subjects', {}).values():
            total_departments += len(dept_list)
    
    return jsonify({
        'success': True,
        'stats': {
            'teachers': teacher_count,
            'students': student_count,
            'subjects': total_subjects,
            'department_assignments': total_departments
        }
    })

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'success': True, 'message': 'Backend is running!'})

@app.route('/api/check', methods=['GET'])
def check():
    return jsonify({'status': 'ok', 'message': 'Server is alive'})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Attendance Management System Backend...")
    print("=" * 60)
    print("Database file:", DB_FILE)
    db = load_database()
    print("Database loaded successfully!")
    print("\n" + "=" * 60)
    print("DEFAULT USERS AVAILABLE:")
    print("=" * 60)
    print("1. Admin:     ADMIN_001 / admin123")
    print("2. Teacher:   TCH_001   / teacher123")
    print("3. Student:   STU_001   / student123")
    print("\n" + "=" * 60)
    print("SERVER URL: http://localhost:5000")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server")
    
    # Run on all network interfaces
    app.run(debug=True, port=5000, host='0.0.0.0')
