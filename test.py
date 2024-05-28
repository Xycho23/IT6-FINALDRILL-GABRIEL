import requests

# Base URL of your Flask application
BASE_URL = 'http://localhost:5000'

# Function to perform login and get JWT token
def get_token():
    url = BASE_URL + '/'
    response = requests.post(url, auth=('admin', 'admin123'))
    if response.status_code == 200:
        return response.json()['token']
    else:
        print('Failed to get token')
        return None

# Function to perform a GET request with JWT token
def authorized_get(endpoint, token):
    url = BASE_URL + endpoint
    headers = {'x-access-token': token}
    response = requests.get(url, headers=headers)
    return response

# Test the '/login' endpoint
def test_login():
    token = get_token()
    if token:
        print('Login successful. Token:', token)
    else:
        print('Login failed')

# Test a protected endpoint with JWT token
def test_protected_endpoint(endpoint, expected_status_code):
    token = get_token()
    if token:
        response = authorized_get(endpoint, token)
        if response.status_code == expected_status_code:
            print(f'Test passed for endpoint {endpoint}. Status code: {expected_status_code}')
        else:
            print(f'Test failed for endpoint {endpoint}. Expected status code: {expected_status_code}. Actual status code: {response.status_code}')
    else:
        print('Test failed. Unable to get JWT token.')

if __name__ == '__main__':
    # Run test cases
    test_login()
    test_protected_endpoint('/users', 200)  # Example: test the '/users' endpoint with expected status code 200
    test_protected_endpoint('/orders', 401)  # Example: test the '/orders' endpoint with expected status code 401 (unauthorized)
