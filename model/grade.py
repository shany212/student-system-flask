from database.db_config import execute_query

def get_grades_by_student(student_id):
    """Get all grades for a student."""
    query = """
    SELECT g.id, g.student_id, g.course_id, g.score, g.semester, 
           s.name as student_name, c.name as course_name
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN courses c ON g.course_id = c.id
    WHERE g.student_id = %s
    ORDER BY g.semester DESC, c.name
    """
    return execute_query(query, (student_id,))

def get_grades_by_course(course_id):
    """Get all grades for a course."""
    query = """
    SELECT g.id, g.student_id, g.course_id, g.score, g.semester, 
           s.name as student_name, c.name as course_name
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN courses c ON g.course_id = c.id
    WHERE g.course_id = %s
    ORDER BY g.score DESC, s.name
    """
    return execute_query(query, (course_id,))

def get_grade(student_id, course_id, semester=None):
    """Get a specific grade."""
    if semester:
        query = """
        SELECT * FROM grades WHERE student_id = %s AND course_id = %s AND semester = %s
        """
        grades = execute_query(query, (student_id, course_id, semester))
    else:
        query = """
        SELECT * FROM grades WHERE student_id = %s AND course_id = %s 
        ORDER BY semester DESC LIMIT 1
        """
        grades = execute_query(query, (student_id, course_id))
    
    return grades[0] if grades and len(grades) > 0 else None

def add_grade(student_id, course_id, score, semester):
    """Add or update a grade."""
    # Check if grade already exists
    existing = get_grade(student_id, course_id, semester)
    
    if existing:
        # Update existing grade
        query = """
        UPDATE grades SET score = %s WHERE id = %s
        """
        execute_query(query, (score, existing['id']), fetch=False)
        return True, "Grade updated successfully"
    else:
        # Add new grade
        query = """
        INSERT INTO grades (student_id, course_id, score, semester) 
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (student_id, course_id, score, semester), fetch=False)
        return True, "Grade added successfully"

def update_grade(grade_id, score):
    """Update a grade by ID."""
    query = "UPDATE grades SET score = %s WHERE id = %s"
    execute_query(query, (score, grade_id), fetch=False)
    return True, "Grade updated successfully"

def delete_grade(grade_id):
    """Delete a grade."""
    query = "DELETE FROM grades WHERE id = %s"
    execute_query(query, (grade_id,), fetch=False)
    return True, "Grade deleted successfully"

def delete_student_grades(student_id):
    """Delete all grades for a student."""
    query = "DELETE FROM grades WHERE student_id = %s"
    execute_query(query, (student_id,), fetch=False)
    return True, "Student grades deleted successfully"

def get_student_average(student_id):
    """Get a student's average grade."""
    query = """
    SELECT AVG(score) as average 
    FROM grades 
    WHERE student_id = %s
    """
    result = execute_query(query, (student_id,))
    return result[0]['average'] if result and result[0]['average'] else 0

def import_grades_from_csv(grades_data):
    """Import grades from CSV data."""
    success_count = 0
    error_count = 0
    
    for row in grades_data:
        student_id = row.get('student_id')
        course_id = row.get('course_id')
        score = row.get('score')
        semester = row.get('semester')
        
        if not all([student_id, course_id, score, semester]):
            error_count += 1
            continue
            
        try:
            success, _ = add_grade(student_id, course_id, float(score), semester)
            if success:
                success_count += 1
            else:
                error_count += 1
        except Exception:
            error_count += 1
    
    return success_count, error_count 