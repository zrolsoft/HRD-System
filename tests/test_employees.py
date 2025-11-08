import json

def test_get_employees_empty(client):
    """Test getting employees when none exist"""
    response = client.get('/api/employees')
    assert response.status_code == 200
    assert response.json == []

def test_create_employee(client):
    """Test creating a new employee"""
    # Create a department first
    dept_data = {'name': 'Engineering'}
    dept_response = client.post('/api/departments',
                                 data=json.dumps(dept_data),
                                 content_type='application/json')
    dept_id = dept_response.json['id']
    
    # Create an employee
    emp_data = {
        'employee_id': 'EMP001',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'position': 'Software Engineer',
        'department_id': dept_id
    }
    response = client.post('/api/employees',
                          data=json.dumps(emp_data),
                          content_type='application/json')
    assert response.status_code == 201
    assert response.json['employee_id'] == 'EMP001'
    assert response.json['first_name'] == 'John'
    assert response.json['email'] == 'john.doe@example.com'

def test_get_employee(client):
    """Test getting a specific employee"""
    # Create an employee
    emp_data = {
        'employee_id': 'EMP002',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com'
    }
    create_response = client.post('/api/employees',
                                   data=json.dumps(emp_data),
                                   content_type='application/json')
    emp_id = create_response.json['id']
    
    # Get the employee
    response = client.get(f'/api/employees/{emp_id}')
    assert response.status_code == 200
    assert response.json['first_name'] == 'Jane'

def test_update_employee(client):
    """Test updating an employee"""
    # Create an employee
    emp_data = {
        'employee_id': 'EMP003',
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'email': 'bob.johnson@example.com'
    }
    create_response = client.post('/api/employees',
                                   data=json.dumps(emp_data),
                                   content_type='application/json')
    emp_id = create_response.json['id']
    
    # Update the employee
    update_data = {'position': 'Senior Developer'}
    response = client.put(f'/api/employees/{emp_id}',
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json['position'] == 'Senior Developer'

def test_delete_employee(client):
    """Test deleting an employee"""
    # Create an employee
    emp_data = {
        'employee_id': 'EMP004',
        'first_name': 'Alice',
        'last_name': 'Williams',
        'email': 'alice.williams@example.com'
    }
    create_response = client.post('/api/employees',
                                   data=json.dumps(emp_data),
                                   content_type='application/json')
    emp_id = create_response.json['id']
    
    # Delete the employee
    response = client.delete(f'/api/employees/{emp_id}')
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f'/api/employees/{emp_id}')
    assert get_response.status_code == 404

def test_create_employee_missing_field(client):
    """Test creating an employee with missing required field"""
    emp_data = {
        'first_name': 'John',
        'last_name': 'Doe'
        # Missing email and employee_id
    }
    response = client.post('/api/employees',
                          data=json.dumps(emp_data),
                          content_type='application/json')
    assert response.status_code == 400

def test_create_employee_duplicate_email(client):
    """Test creating an employee with duplicate email"""
    emp_data = {
        'employee_id': 'EMP005',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'duplicate@example.com'
    }
    client.post('/api/employees',
                data=json.dumps(emp_data),
                content_type='application/json')
    
    # Try to create another with same email
    emp_data2 = {
        'employee_id': 'EMP006',
        'first_name': 'Another',
        'last_name': 'User',
        'email': 'duplicate@example.com'
    }
    response = client.post('/api/employees',
                          data=json.dumps(emp_data2),
                          content_type='application/json')
    assert response.status_code == 409
