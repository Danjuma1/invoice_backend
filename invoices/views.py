from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, Invoice
from .serializers import (
    CustomerSerializer,
    InvoiceSerializer,
    InvoiceCreateUpdateSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    # ViewSet for managing customers.
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ['get', 'post', 'head', 'options']


class InvoiceViewSet(viewsets.ModelViewSet):
    # ViewSet for managing invoices.
    queryset = Invoice.objects.all()

    def get_serializer_class(self):
        # Return appropriate serializer based on action.
        if self.action in ['create', 'partial_update']:
            return InvoiceCreateUpdateSerializer
        return InvoiceSerializer

    def get_queryset(self):
        # Optimized queryset with select_related and prefetch_related.
        queryset = Invoice.objects.select_related('customer').prefetch_related('items')
        
        # Optional filtering by status
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset

    @action(detail=True, methods=['patch'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        # Mark an invoice as paid.
        invoice = self.get_object()
        invoice.status = 'paid'
        invoice.save()
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
