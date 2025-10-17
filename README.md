# Django Invoicing Backend

A Django REST Framework backend for managing customers and invoices with line items.

_Being an assessment submitted to DevRecruit for the position of Django Fullstack Developer on Friday 17th October, 2025_

## Features
- Customer management (create, list)
- Invoice creation with nested line items
- Automatic calculation of invoice totals
- Date validation to ensure due_date >= issue_date
- Invoice status tracking and marking (pending, paid, overdue)
- Unit tests

## Tech Stack Used

- Python 
- Django
- Django REST Framework
- SQLite (default)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd invoicing_project
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows (CMD or Powershell):
venv\Scripts\activate

# On Windows (Bash):
source venv/Scripts/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional - for Admin)
```bash
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
python manage.py loaddata sample_data.json
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Customers

**POST /api/customers/** - Create a customer
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**GET /api/customers/** - List all customers

**GET /api/customers/{id}/** - Get customer details

### Invoices

**POST /api/invoices/** - Create an invoice with line items
```json
{
  "customer": 1,
  "issue_date": "2025-10-17",
  "due_date": "2025-10-25",
  "status": "pending",
  "items": [
    {
      "description": "Web Development",
      "quantity": 5,
      "unit_price": "100000.00"
    },
    {
      "description": "Design Services",
      "quantity": 2,
      "unit_price": "150000.00"
    }
  ]
}
```

**GET /api/invoices/** - List all invoices (with optional status filter)
```
GET /api/invoices/?status=pending
```

**GET /api/invoices/{id}/** - Get invoice details with items and total

**PATCH /api/invoices/{id}/** - Update invoice status
```json
{
  "status": "overdue"
}
```

**PATCH /api/invoices/{id}/mark-paid/** - Mark invoice as paid (convenience endpoint)

## Validation

The API enforces the following validations:

1. **Empty Line Items**: Invoices must have at least one line item
2. **Date Validation**: Due date must be on or after the issue date
3. **Email Uniqueness**: Each customer email must be unique
4. **Positive Quantities**: Invoice item quantities must be positive integers

## Running Tests

```bash
python manage.py test invoices
```

For verbose output:
```bash
python manage.py test invoices -v 2
```


## Django Admin

Access the admin panel at `http://localhost:8000/admin/` with your superuser credentials.

## Built By

Habeebulllah Akorede 

## License

MIT