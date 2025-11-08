# HRD System

A Human Resources Development (HRD) System built with Flask and SQLAlchemy.

## Features

- **Employee Management**: Create, read, update, and delete employee records
- **Department Management**: Manage organizational departments
- **RESTful API**: Clean API endpoints for all operations
- **Data Validation**: Input validation and error handling
- **SQLite Database**: Lightweight database for data persistence

## Project Structure

```
HRD-System/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   └── routes/
│       ├── employees.py     # Employee endpoints
│       └── departments.py   # Department endpoints
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zrolsoft/HRD-System.git
cd HRD-System
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

The application will start on `http://localhost:5000`

## API Endpoints

### Employees

- `GET /api/employees` - Get all employees
- `GET /api/employees/<id>` - Get a specific employee
- `POST /api/employees` - Create a new employee
- `PUT /api/employees/<id>` - Update an employee
- `DELETE /api/employees/<id>` - Delete an employee

### Departments

- `GET /api/departments` - Get all departments
- `GET /api/departments/<id>` - Get a specific department
- `POST /api/departments` - Create a new department
- `PUT /api/departments/<id>` - Update a department
- `DELETE /api/departments/<id>` - Delete a department
- `GET /api/departments/<id>/employees` - Get all employees in a department

## Example Usage

### Create a Department

```bash
curl -X POST http://localhost:5000/api/departments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering",
    "description": "Software development team"
  }'
```

### Create an Employee

```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "555-1234",
    "position": "Software Engineer",
    "department_id": 1,
    "hire_date": "2024-01-15",
    "salary": 75000,
    "status": "active"
  }'
```

### Get All Employees

```bash
curl http://localhost:5000/api/employees
```

## Database Schema

### Employee Table
- `id` (Primary Key)
- `employee_id` (Unique)
- `first_name`
- `last_name`
- `email` (Unique)
- `phone`
- `position`
- `department_id` (Foreign Key)
- `hire_date`
- `salary`
- `status` (active/inactive/terminated)
- `created_at`
- `updated_at`

### Department Table
- `id` (Primary Key)
- `name` (Unique)
- `description`
- `created_at`
- `updated_at`

## Development

### Running Tests

```bash
pytest tests/
```

### Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///hrd_system.db
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request