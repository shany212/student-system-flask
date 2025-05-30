# 学生成绩管理系统

一个基于Flask的学生成绩管理系统，提供了学生信息管理、课程管理和成绩管理等功能。

## 功能特点

- 用户认证与授权（管理员/普通用户）
- 学生信息管理（添加、查看、编辑、删除）
- 课程信息管理（添加、查看、编辑、删除）
- 成绩管理（添加、查看、编辑、删除）
- 批量导入成绩（CSV文件）
- 成绩数据可视化（图表展示）
- 响应式设计，适配各种设备

## 技术栈

- 后端：Python 3.6+ / Flask 2.0+
- 数据库：MySQL
- 前端：Bootstrap 5 / Chart.js / Bootstrap Icons

## 系统要求

- Python 3.6+
- MySQL 5.7+
- pip (Python包管理器)

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/student-system-flask.git
cd student-system-flask
```

### 2. 创建虚拟环境

```bash
python -m venv venv
```

#### Windows
```bash
venv\Scripts\activate
```

#### macOS/Linux
```bash
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

1. 使用MySQL创建数据库:

```sql
CREATE DATABASE student_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改`database/db_config.py`中的数据库连接配置:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'student_management',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}
```

3. 运行SQL脚本创建表和初始数据:

```bash
mysql -u your_username -p student_management < database/schema.sql
```

### 5. 运行应用

```bash
python app.py
```

访问 http://localhost:5000 即可使用系统

## 默认账户

- 管理员: admin / admin123
- 普通用户: student / student123

## 项目结构

```
student-system-flask/
├── app.py               # 主应用程序
├── database/            # 数据库相关
│   ├── db_config.py     # 数据库配置
│   └── schema.sql       # 数据库架构
├── model/               # 数据模型
│   ├── course.py        # 课程模型
│   ├── grade.py         # 成绩模型
│   ├── student.py       # 学生模型
│   └── user.py          # 用户模型
├── static/              # 静态文件
│   ├── css/             # CSS样式
│   └── js/              # JavaScript脚本
├── templates/           # 模板文件
│   ├── base.html        # 基础模板
│   ├── dashboard.html   # 控制面板
│   ├── login.html       # 登录页面
│   ├── register.html    # 注册页面
│   ├── courses/         # 课程相关页面
│   ├── grades/          # 成绩相关页面
│   └── students/        # 学生相关页面
├── uploads/             # 上传文件目录
├── requirements.txt     # 项目依赖
└── README.md            # 项目说明文档
```

## 功能截图

(此处可添加系统截图)

## 许可证

MIT
