from database.db_config import execute_query

def get_all_students():
    """Get all students."""
    query = "SELECT * FROM students ORDER BY id"
    return execute_query(query)

def get_student_by_id(student_id):
    """Get a student by ID."""
    query = "SELECT * FROM students WHERE id = %s"
    students = execute_query(query, (student_id,))
    return students[0] if students and len(students) > 0 else None

def create_student(student_id, name, gender, birthday=None, email=None, phone=None, address=None):
    """Create a new student."""
    # Check if student_id already exists
    existing = get_student_by_id(student_id)
    if existing:
        return False, "Student ID already exists"
    
    query = """
    INSERT INTO students (id, name, gender, birthday, email, phone, address) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (student_id, name, gender, birthday, email, phone, address), fetch=False)
    return True, "Student created successfully"

def update_student(student_id, name=None, gender=None, birthday=None, email=None, phone=None, address=None):
    """Update student information."""
    # Get current student data
    student = get_student_by_id(student_id)
    if not student:
        return False, "Student not found"
    
    # Use current values if new ones not provided
    name = name if name is not None else student['name']
    gender = gender if gender is not None else student['gender']
    birthday = birthday if birthday is not None else student['birthday']
    email = email if email is not None else student['email']
    phone = phone if phone is not None else student['phone']
    address = address if address is not None else student['address']
    
    query = """
    UPDATE students 
    SET name = %s, gender = %s, birthday = %s, email = %s, phone = %s, address = %s 
    WHERE id = %s
    """
    execute_query(query, (name, gender, birthday, email, phone, address, student_id), fetch=False)
    return True, "Student updated successfully"

def delete_student(student_id):
    """Delete a student."""
    query = "DELETE FROM students WHERE id = %s"
    execute_query(query, (student_id,), fetch=False)
    return True, "Student deleted successfully" 