# Flask JWT Authentication with MySQL

This is a Flask application that demonstrates JWT (JSON Web Token) authentication with MySQL database integration. It provides endpoints for user authentication, searching users, orders, products, suppliers, and total sales records, as well as CRUD operations for users.

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.x
- Flask
- Flask-MySQLdb
- PyJWT

You also need a MySQL server running locally with the following configuration:
- User: root
- Password: PHW#84#jeor
- Database: datasets
- Host: localhost
- Port: 3306

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Xycho23/IT6-FINAL_DRILL-GABRIEL.git

2. Install the required dependencies:
pip install Flask Flask-MySQLdb PyJWT

3. Run the Flask application:
python app.py


The application will run on http://127.0.0.1:5000/ by default.

Usage
Authentication
To authenticate, send a POST request to /login endpoint with Basic Auth credentials (admin/admin123). It will return a JWT token that you can use to access protected endpoints.
Can be use Gitbash
Example:
curl -X POST -u admin:admin123 http://localhost:5000/login


Endpoints
GET /users: Get all users.
POST /users: Create a new user.
GET /users/<id>: Get user by ID.
PUT /users/<id>: Update user by ID.
DELETE /users/<id>: Delete user by ID.
GET /users/search?id=<id>: Search for a user by ID.
GET /users/<id>/orders: Get orders of a user by ID.
GET /orders: Get all orders.
GET /orders/search?id=<id>: Search for an order by ID.
GET /products: Get all products.
GET /products/search?id=<id>: Search for a product by ID.
GET /supplier: Get all suppliers.
GET /supplier/search?id=<id>: Search for a supplier by ID.
GET /total_sales: Get total sales records.
GET /total_sales/search?id=<id>: Search for a total sales record by ID.

# Flask JWT Authentication with MySQL

Welcome to our Flask application! This project showcases how to implement JWT (JSON Web Token) authentication with MySQL integration. We've built various endpoints for user authentication, searching users, orders, products, suppliers, and total sales records. Additionally, we've included CRUD (Create, Read, Update, Delete) operations for users.

## Development History

### API (api.py)

1. **Kickstarting the Journey**: We began by setting up the basic structure of our Flask application.
2. **Connecting to Our Database**: Configured our application to communicate with MySQL for data storage.
3. **Securing Access with JWT**: Implemented JWT authentication to secure our endpoints and ensure user privacy.
4. **Empowering User Management**: Created endpoints for managing users, allowing for creation, viewing, updating, and deletion.
5. **Dealing with Errors Gracefully**: Improved error handling to provide clear feedback to users when something goes wrong.
6. **Finding What You Need**: Added search functionality across various entities, making it easy to locate specific records.
7. **Cleaning Up Our Code**: Refactored our codebase to improve readability and maintainability.
8. **Making Queries More Efficient**: Optimized our database queries to enhance performance and reduce load times.
9. **Documenting for Clarity**: Added detailed documentation to our endpoints to guide users on their usage.
10. **Squashing Bugs**: Resolved an issue related to authentication, ensuring a smooth user experience.
11. **Staying Up-to-Date**: Updated our dependencies to leverage the latest features and security patches.
12. **Keeping Things Secure**: Enhanced security measures by implementing input validation to prevent potential vulnerabilities.
13. **Presenting Data Nicely**: Formatted our API responses for a cleaner and more organized presentation.
14. **Handling Edge Cases**: Addressed edge cases to ensure our application remains robust in all scenarios.
15. **Logging for Insight**: Augmented our logging mechanism to capture valuable information for troubleshooting and monitoring.

### Test Suite (test.py)

1. **Laying the Foundation**: Started building our test suite to automate the testing of our API endpoints.
2. **Ensuring Smooth Authentication**: Created tests to verify the login functionality, ensuring users can securely authenticate.
3. **Testing User Operations**: Verified the correctness of user-related operations such as creation, retrieval, updating, and deletion.
4. **Searching with Confidence**: Ensured our search endpoints return accurate results, enhancing user experience.
5. **Securing Protected Endpoints**: Validated authentication mechanisms for protected endpoints, safeguarding sensitive data.
6. **Handling Errors with Care**: Tested error responses to ensure users receive helpful feedback when encountering issues.
7. **Extending Test Coverage**: Expanded our test suite to cover additional scenarios, ensuring comprehensive testing.
8. **Improving Readability**: Refactored our test code for better organization and clarity, making it easier to understand.
9. **Setting the Stage**: Established reusable fixtures to streamline test setup and execution.
10. **Verifying Product Operations**: Tested CRUD operations for products, ensuring product-related functionalities work as expected.
11. **Validating Order Processes**: Verified the functionality related to orders and transactions, maintaining data integrity.
12. **Ensuring Supplier Operations**: Validated supplier-related endpoints to ensure seamless interaction with supplier data.
13. **Checking Total Sales Records**: Ensured accurate retrieval and searching of total sales records for reporting purposes.
14. **Refining Assertions**: Enhanced assertion statements for more informative test failures, facilitating debugging.
15. **Wrapping Up Testing**: Completed our test suite by reviewing and polishing test cases to ensure reliability.

## Installation and Usage

For installation instructions and usage guidelines, refer to the [Installation](#installation) and [Usage](#usage) sections in this README.

