-- Sample data for the student management system

-- Use the database
USE student_management;

-- Insert admin user
INSERT INTO users (username, password, is_admin) VALUES
('admin', 'admin123', TRUE); -- password: 'admin123'

-- Insert normal user
INSERT INTO users (username, password, is_admin) VALUES
('student', '46a0baab5ba3bb3655784daaa839fc82e3a3afedf8adf5a84801a1e8f7a8ce25', FALSE); -- password: 'student123'

-- Insert sample students
INSERT INTO students (id, name, gender, birthday, email, phone, address) VALUES
('S001', '张三', 'male', '2000-05-15', 'zhangsan@example.com', '13800138001', '北京市海淀区'),
('S002', '李四', 'female', '2001-02-20', 'lisi@example.com', '13800138002', '上海市徐汇区'),
('S003', '王五', 'male', '2000-09-10', 'wangwu@example.com', '13800138003', '广州市天河区'),
('S004', '赵六', 'female', '2001-11-05', 'zhaoliu@example.com', '13800138004', '深圳市南山区'),
('S005', '钱七', 'male', '2002-03-25', 'qianqi@example.com', '13800138005', '杭州市西湖区');

-- Insert sample courses
INSERT INTO courses (id, name, credit, description) VALUES
('C001', '高等数学', 4.0, '本课程涵盖微积分、线性代数等内容，是理工科学生的必修课程。'),
('C002', '大学英语', 3.0, '本课程注重培养学生的英语听说读写能力，提高语言综合应用能力。'),
('C003', '计算机基础', 3.0, '本课程介绍计算机的基本原理、操作系统、办公软件等内容。'),
('C004', '数据结构', 4.0, '本课程讲解各种数据结构和算法，培养学生的编程和解决问题能力。'),
('C005', '数据库原理', 3.5, '本课程介绍数据库的设计、使用和优化，包括SQL语言、关系模型等内容。');

-- Insert sample grades
INSERT INTO grades (student_id, course_id, score, semester) VALUES
('S001', 'C001', 85.5, '2022-2023-1'),
('S001', 'C002', 92.0, '2022-2023-1'),
('S001', 'C003', 78.5, '2022-2023-1'),
('S001', 'C004', 88.0, '2022-2023-2'),
('S001', 'C005', 90.5, '2022-2023-2'),

('S002', 'C001', 76.0, '2022-2023-1'),
('S002', 'C002', 95.5, '2022-2023-1'),
('S002', 'C003', 82.0, '2022-2023-1'),
('S002', 'C004', 79.5, '2022-2023-2'),
('S002', 'C005', 86.0, '2022-2023-2'),

('S003', 'C001', 92.5, '2022-2023-1'),
('S003', 'C002', 85.0, '2022-2023-1'),
('S003', 'C003', 90.0, '2022-2023-1'),
('S003', 'C004', 94.5, '2022-2023-2'),
('S003', 'C005', 88.5, '2022-2023-2'),

('S004', 'C001', 65.0, '2022-2023-1'),
('S004', 'C002', 72.5, '2022-2023-1'),
('S004', 'C003', 68.0, '2022-2023-1'),
('S004', 'C004', 59.5, '2022-2023-2'),
('S004', 'C005', 70.0, '2022-2023-2'),

('S005', 'C001', 55.5, '2022-2023-1'),
('S005', 'C002', 62.0, '2022-2023-1'),
('S005', 'C003', 59.5, '2022-2023-1'),
('S005', 'C004', 67.0, '2022-2023-2'),
('S005', 'C005', 60.5, '2022-2023-2');

-- Add different semester data
INSERT INTO grades (student_id, course_id, score, semester) VALUES
('S001', 'C001', 88.5, '2023-2024-1'),
('S002', 'C001', 81.0, '2023-2024-1'),
('S003', 'C001', 94.0, '2023-2024-1'),
('S004', 'C001', 70.5, '2023-2024-1'),
('S005', 'C001', 62.0, '2023-2024-1');

-- Add some failing grades for distribution
INSERT INTO grades (student_id, course_id, score, semester) VALUES
('S004', 'C002', 55.0, '2023-2024-1'),
('S004', 'C003', 48.5, '2023-2024-1'),
('S005', 'C002', 42.0, '2023-2024-1'),
('S005', 'C004', 38.5, '2023-2024-1'); 