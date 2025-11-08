import json

def test_get_departments_empty(client):
    """Test getting departments when none exist"""
    response = client.get('/api/departments')
    assert response.status_code == 200
    assert response.json == []

def test_create_department(client):
    """Test creating a new department"""
    data = {
        'name': 'Engineering',
        'description': 'Software development team'
    }
    response = client.post('/api/departments',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 201
    assert response.json['name'] == 'Engineering'
    assert response.json['description'] == 'Software development team'
    assert 'id' in response.json

def test_get_department(client):
    """Test getting a specific department"""
    # Create a department first
    data = {'name': 'HR', 'description': 'Human Resources'}
    create_response = client.post('/api/departments',
                                   data=json.dumps(data),
                                   content_type='application/json')
    dept_id = create_response.json['id']
    
    # Get the department
    response = client.get(f'/api/departments/{dept_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'HR'

def test_update_department(client):
    """Test updating a department"""
    # Create a department
    data = {'name': 'IT', 'description': 'Information Technology'}
    create_response = client.post('/api/departments',
                                   data=json.dumps(data),
                                   content_type='application/json')
    dept_id = create_response.json['id']
    
    # Update the department
    update_data = {'description': 'Updated IT Department'}
    response = client.put(f'/api/departments/{dept_id}',
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json['description'] == 'Updated IT Department'

def test_delete_department(client):
    """Test deleting a department"""
    # Create a department
    data = {'name': 'Marketing'}
    create_response = client.post('/api/departments',
                                   data=json.dumps(data),
                                   content_type='application/json')
    dept_id = create_response.json['id']
    
    # Delete the department
    response = client.delete(f'/api/departments/{dept_id}')
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f'/api/departments/{dept_id}')
    assert get_response.status_code == 404

def test_create_department_duplicate_name(client):
    """Test creating a department with duplicate name"""
    data = {'name': 'Sales'}
    client.post('/api/departments',
                data=json.dumps(data),
                content_type='application/json')
    
    # Try to create another with same name
    response = client.post('/api/departments',
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 409
