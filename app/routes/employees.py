from flask import Blueprint, request, jsonify
from app import db
from app.models import Employee
from datetime import datetime
from sqlalchemy.exc import IntegrityError

bp = Blueprint('employees', __name__, url_prefix='/api/employees')

@bp.route('', methods=['GET'])
def get_employees():
    """Get all employees"""
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_employee(id):
    """Get a specific employee"""
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict()), 200

@bp.route('', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['employee_id', 'first_name', 'last_name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        employee = Employee(
            employee_id=data['employee_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            position=data.get('position'),
            department_id=data.get('department_id'),
            hire_date=datetime.fromisoformat(data['hire_date']) if data.get('hire_date') else None,
            salary=data.get('salary'),
            status=data.get('status', 'active')
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify(employee.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Employee ID or email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    """Update an employee"""
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    
    try:
        # Update fields if provided
        if 'first_name' in data:
            employee.first_name = data['first_name']
        if 'last_name' in data:
            employee.last_name = data['last_name']
        if 'email' in data:
            employee.email = data['email']
        if 'phone' in data:
            employee.phone = data['phone']
        if 'position' in data:
            employee.position = data['position']
        if 'department_id' in data:
            employee.department_id = data['department_id']
        if 'hire_date' in data:
            employee.hire_date = datetime.fromisoformat(data['hire_date']) if data['hire_date'] else None
        if 'salary' in data:
            employee.salary = data['salary']
        if 'status' in data:
            employee.status = data['status']
        
        db.session.commit()
        return jsonify(employee.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """Delete an employee"""
    employee = Employee.query.get_or_404(id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
