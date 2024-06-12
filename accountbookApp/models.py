from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='income')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}"