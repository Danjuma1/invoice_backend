from django.db import models
from django.core.exceptions import ValidationError

class Customer(models.Model):
    # Customer model to store customer details.
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    

class Invoice(models.Model):
    # Invoive model representing an invoice issued to a customer.
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        # Validates that due_date is after issue_date.
        if self.due_date < self.issue_date:
            raise ValidationError('Due date must be on or after the issue date.')

    def __str__(self):
        return f'Invoice {self.id} - {self.customer.name}'

    def save(self, *args, **kwargs):
        # Ensures the validation is done before saving.
        self.full_clean()
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    # Model Representing a line item in an invoice.
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.description} - {self.quantity} x {self.unit_price}'

    @property
    def total(self):
        # Calculates the total price for this line item.
        return self.quantity * self.unit_price
