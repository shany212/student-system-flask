from database.db_config import execute_query

def get_all_courses():
    """Get all courses."""
    query = "SELECT * FROM courses ORDER BY id"
    return execute_query(query)

def get_course_by_id(course_id):
    """Get a course by ID."""
    query = "SELECT * FROM courses WHERE id = %s"
    courses = execute_query(query, (course_id,))
    return courses[0] if courses and len(courses) > 0 else None

def create_course(course_id, name, credit, description=None):
    """Create a new course."""
    # Check if course_id already exists
    existing = get_course_by_id(course_id)
    if existing:
        return False, "Course ID already exists"
    
    query = """
    INSERT INTO courses (id, name, credit, description) 
    VALUES (%s, %s, %s, %s)
    """
    execute_query(query, (course_id, name, credit, description), fetch=False)
    return True, "Course created successfully"

def update_course(course_id, name=None, credit=None, description=None):
    """Update course information."""
    # Get current course data
    course = get_course_by_id(course_id)
    if not course:
        return False, "Course not found"
    
    # Use current values if new ones not provided
    name = name if name is not None else course['name']
    credit = credit if credit is not None else course['credit']
    description = description if description is not None else course['description']
    
    query = """
    UPDATE courses 
    SET name = %s, credit = %s, description = %s 
    WHERE id = %s
    """
    execute_query(query, (name, credit, description, course_id), fetch=False)
    return True, "Course updated successfully"

def delete_course(course_id):
    """Delete a course."""
    query = "DELETE FROM courses WHERE id = %s"
    execute_query(query, (course_id,), fetch=False)
    return True, "Course deleted successfully" 