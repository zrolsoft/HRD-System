from flask import Blueprint, request, jsonify
from app import db
from app.models import Department
from sqlalchemy.exc import IntegrityError

bp = Blueprint('departments', __name__, url_prefix='/api/departments')

@bp.route('', methods=['GET'])
def get_departments():
    """Get all departments"""
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_department(id):
    """Get a specific department"""
    department = Department.query.get_or_404(id)
    return jsonify(department.to_dict()), 200

@bp.route('', methods=['POST'])
def create_department():
    """Create a new department"""
    data = request.get_json()
    
    # Validate required fields
    if 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    try:
        department = Department(
            name=data['name'],
            description=data.get('description')
        )
        
        db.session.add(department)
        db.session.commit()
        
        return jsonify(department.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Department name already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
def update_department(id):
    """Update a department"""
    department = Department.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            department.name = data['name']
        if 'description' in data:
            department.description = data['description']
        
        db.session.commit()
        return jsonify(department.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Department name already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete_department(id):
    """Delete a department"""
    department = Department.query.get_or_404(id)
    
    # Check if department has employees
    if department.employees:
        return jsonify({'error': 'Cannot delete department with employees'}), 400
    
    try:
        db.session.delete(department)
        db.session.commit()
        return jsonify({'message': 'Department deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>/employees', methods=['GET'])
def get_department_employees(id):
    """Get all employees in a department"""
    department = Department.query.get_or_404(id)
    return jsonify([emp.to_dict() for emp in department.employees]), 200
