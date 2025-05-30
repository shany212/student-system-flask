-- Drop database if exists and create a new one
DROP DATABASE IF EXISTS student_management;
CREATE DATABASE student_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_management;

-- Users table - stores user authentication information
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Students table - stores student information
CREATE TABLE students (
    id VARCHAR(20) PRIMARY KEY COMMENT 'Student ID',
    name VARCHAR(100) NOT NULL,
    gender ENUM('male', 'female', 'other') NOT NULL,
    birthday DATE NULL,
    email VARCHAR(100) NULL,
    phone VARCHAR(20) NULL,
    address TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP
);

-- Courses table - stores course information
CREATE TABLE courses (
    id VARCHAR(20) PRIMARY KEY COMMENT 'Course ID',
    name VARCHAR(100) NOT NULL,
    credit DECIMAL(3,1) NOT NULL DEFAULT 1.0,
    description TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP
);

-- Grades table - stores student grades for courses
CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(20) NOT NULL,
    score DECIMAL(5,2) NULL,
    semester VARCHAR(20) NULL COMMENT 'e.g. "Fall 2023"',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY (student_id, course_id, semester)
);

-- Insert admin user
INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin123', TRUE);
INSERT INTO users (username, password, is_admin) VALUES ('student', 'student123', FALSE);

-- Insert sample students
INSERT INTO students (id, name, gender, email, phone) VALUES 
('S001', '张三', 'male', 'zhangsan@example.com', '13800000001'),
('S002', '李四', 'female', 'lisi@example.com', '13800000002'),
('S003', '王五', 'male', 'wangwu@example.com', '13800000003'),
('S004', '赵六', 'female', 'zhaoliu@example.com', '13800000004');

-- Insert sample courses
INSERT INTO courses (id, name, credit, description) VALUES 
('C001', '高等数学', 4.0, '大一必修课程，内容包括极限、微积分、级数等'),
('C002', '大学英语', 3.0, '大一必修课程，提高英语听说读写能力'),
('C003', '计算机基础', 3.0, '计算机基本原理与应用'),
('C004', '数据结构', 4.0, '计算机专业核心课程');

-- Insert sample grades
INSERT INTO grades (student_id, course_id, score, semester) VALUES 
('S001', 'C001', 88.5, '2023-2024-1'),
('S001', 'C002', 92.0, '2023-2024-1'),
('S002', 'C001', 76.5, '2023-2024-1'),
('S002', 'C003', 85.0, '2023-2024-1'),
('S003', 'C002', 90.5, '2023-2024-1'),
('S003', 'C004', 82.0, '2023-2024-1'),
('S004', 'C001', 95.0, '2023-2024-1'),
('S004', 'C004', 88.0, '2023-2024-1'); 