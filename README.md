# Vendor Management System


The Vendor Management System is a Django-based application that enables users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics. This README provides an overview of the project structure, setup instructions, details on using the API endpoints, and authentication.

## Project Structure
```bash
vendor_management_system/
├── db.sqlite3 # SQLite database file
├── manage.py # Django management script
├── requirements.txt # File containing project dependencies
├── vendors/ # Django app for vendor management
└── vendor_management_system/ # Django project settings
```


## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd vendor_management_system
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Apply Migrations
```bash
python manage.py migrate
```
### 4. Create a Superuser 
```bash
python manage.py createsuperuser
```
### 5. Run the Development Server
```bash
python manage.py runserver
```
## API Endpoints
### Vendors
* `POST /api/vendors/`: Create a new vendor.
* `GET /api/vendors/`: List all vendors.
* `GET /api/vendors/<vendor_id>/`: Retrieve details of a specific vendor.
* `PUT /api/vendors/<vendor_id>/`: Update a vendor.
* `DELETE /api/vendors/<vendor_id>/`: Delete a vendor.
### Purchase Orders
* `POST /api/purchase_orders/`: Create a purchase order.
* `GET /api/purchase_orders/`: List all purchase orders with optional filtering by vendor.
* `GET /api/purchase_orders/<po_id>/`: Retrieve details of a specific purchase order.
* `PUT /api/purchase_orders/<po_id>/`: Update a purchase order.
* `DELETE /api/purchase_orders/<po_id>/`: Delete a purchase order.
### Vendor Performance Metrics
* `GET /api/vendors/<vendor_id>/performance/`: Retrieve performance metrics for a specific vendor.
### Historical Performance
* `GET /api/historical-performance/<int:pk>/`: Retrieve historical performance records for a specific vendor.
### Authentication
Token-based authentication is used to secure the API endpoints. To obtain a JWT token:

* <strong>Endpoint:</strong> `POST /api/token/`
* <strong>Request Body:</strong> Include the user's username and password.
* <strong>Response:</strong> If the credentials are valid, the response will contain an access token and a refresh token.
### Example Request Body:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### Example Response:

```json
{
    "access": "<your-access-token>",
    "refresh": "<your-refresh-token>"
}
```
### To access protected endpoints in Postman:

* <strong>Obtain Tokens:</strong> Send a POST request to `/api/token/` with your username and password in the request body. Save the access token received in the response.
* <strong>Set Authorization Header:</strong>
 In your subsequent requests, set the Authorization header to `Bearer <your-access-token>`.
### Example Authorization Header:

```bash
Authorization: Bearer <your-access-token>
```
### Refreshing Tokens:

* If your access token expires, you can use the refresh token to obtain a new access token by sending a POST request to `/api/token/refresh/`.
* Include the refresh token in the request body as follows:
```json
{
    "refresh": "<your-refresh-token>"
}
``` 
