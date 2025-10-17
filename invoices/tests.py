from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Customer, Invoice, InvoiceItem
from rest_framework.test import APIClient
from rest_framework import status

class InvoiceCreationTestCase(TestCase):
    # Test cases for invoice creation.

    def setUp(self):
        # Setting up test data.
        self.client = APIClient()
        self.customer = Customer.objects.create(
            name='John Doe',
            email='john@example.com'
        )

    def test_create_invoice_with_items(self):
        # Test creating an invoice with line items via the API.
        today = timezone.now().date()
        data = {
            'customer': self.customer.id,
            'issue_date': today,
            'due_date': today + timedelta(days=30),
            'status': 'pending',
            'items': [
                {
                    'description': 'Web Development',
                    'quantity': 5,
                    'unit_price': '100000.00'
                },
                {
                    'description': 'Design Services',
                    'quantity': 2,
                    'unit_price': '150000.00'
                }
            ]
        }

        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        invoice = Invoice.objects.first()
        self.assertEqual(invoice.items.count(), 2)

    def test_create_invoice_without_items_fails(self):
        # Test that creating an invoice without items fails.
        today = timezone.now().date()
        data = {
            'customer': self.customer.id,
            'issue_date': today,
            'due_date': today + timedelta(days=30),
            'items': []
        }

        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_due_date_before_issue_date_fails(self):
        # Test that due_date before issue_date is rejected.
        today = timezone.now().date()
        data = {
            'customer': self.customer.id,
            'issue_date': today,
            'due_date': today - timedelta(days=5),
            'items': [
                {
                    'description': 'Service',
                    'quantity': 1,
                    'unit_price': '100.00'
                }
            ]
        }

        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
