from django.db import models

class Affiliate(models.Model):
    DOCUMENT_TYPES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'Número de Identificación Tributaria'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    full_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'affiliate'
        
class Contribution(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('TRANSFER', 'Transfer'),
        ('CARD', 'Card'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contribution_date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contribution'
        indexes = [
            models.Index(fields=['affiliate', 'contribution_date']),
        ]
