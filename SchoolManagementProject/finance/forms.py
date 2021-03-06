from django.forms import inlineformset_factory,modelformset_factory

from corecode.models import AcademicTerm,AcademicSession,StudentClass
from .models import Invoice,InvoiceItem,Receipt

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=['description', 'amount'], extra=1, can_delete=True)

InvoiceReceiptFormset = inlineformset_factory(
    Invoice, Receipt, fields=('amount_paid', 'date_paid', 'comment'), extra=0, can_delete=True
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=1)
