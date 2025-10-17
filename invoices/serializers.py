from rest_framework import serializers
from .models import Customer, Invoice, InvoiceItem
from decimal import Decimal

class InvoiceItemSerializer(serializers.ModelSerializer):
    # Serializer for invoice line items.
    total = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total']
        read_only_fields = ['id', 'total']

    def get_total(self, obj):
        # Calculates and return the total for this item.
        return obj.total


class InvoiceSerializer(serializers.ModelSerializer):
    # Serializer for listing invoices.
    items = InvoiceItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'issue_date', 'due_date', 'status', 'items', 'total_amount', 'created_at']
        read_only_fields = ['id', 'created_at', 'total_amount']

    def get_total_amount(self, obj):
        # Calculates the total amount for the entire invoice.
        return sum(item.total for item in obj.items.all())


class InvoiceCreateUpdateSerializer(serializers.ModelSerializer):
    # Serializer for creating/updating invoices with nested items.
    items = InvoiceItemSerializer(many=True, write_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'issue_date', 'due_date', 'status', 'items', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_items(self, value):
        # Validates that at least one item is provided.
        if not value:
            raise serializers.ValidationError('An invoice must have at least one line item.')
        return value

    def validate(self, data):
        # Validates that due_date is not before issue_date.
        if data['due_date'] < data['issue_date']:
            raise serializers.ValidationError(
                'Due date must be on or after the issue date.'
            )
        return data

    def create(self, validated_data):
        # Creates invoice with nested items.
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        
        return invoice

    def update(self, instance, validated_data):
        # Updates invoice (items are read-only during update).
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    # Serializer for customers.
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
