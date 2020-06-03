from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.forms import widgets
from django.urls import reverse_lazy

from students.models import Student
from .models import *
from .forms import *

# Create your views here.
class InvoiceListView(LoginRequiredMixin,ListView):
    models = Invoice
    template_name = 'finance/invoice_list.html'

    def get_queryset(self):
        return Invoice.objects.order_by('student')[:5]

class InvoiceCreateView(LoginRequiredMixin,CreateView):
    model = Invoice
    fields = '__all__'
    success_message = 'New Invoice added Successfully'

    def get_context_data(self,**kwargs):
        context = super(InvoiceCreateView,self).get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = InvoiceItemFormset(self.request.POST, prefix='invoiceitem_set')

        else:
            context['items'] = InvoiceItemFormset(prefix='invoiceitem_set')
        return context

    def form_valid(self,form):
        context = self.get_context_data()
        formset = context['items']
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)

class InvoiceDetailView(LoginRequiredMixin,DetailView):
    model = Invoice
    fields ='__all__'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView,self).get_context_data(**kwargs)
        context['receipts'] = Receipt.objects.filter(invoice=self.object)
        context['item'] = InvoiceItem.objects.filter(invoice=self.object)
        return context

class InvoiceUpdateView(LoginRequiredMixin,UpdateView):
    model = Invoice
    fields = ['student','session','term','class_for','balance_from_previous_term']

    def get_context_data(self,**kwargs):
        context = super(InvoiceUpdateView,self).get_context_data(**kwargs)
        if self.request.POST:
            context['receipts'] = InvoiceReceiptFormset(self.request.POST,instance=self.object)
            context['items'] = InvoiceItemFormset(self.request.POST,instance=self.object)
        else:
            context['receipts'] = InvoiceReceiptFormset(instance=self.object)
            context['items'] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self,form):
        context = self.get_context_data()
        formset = context['receipts']
        itemformset = context['items']
        if form.is_valid() and formset.is_valid() and itemformset.is_valid():
            form.save()
            formset.save()
            itemformset.save()
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin,DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice-list')


class ReceiptCreateView(LoginRequiredMixin,CreateView):
    model = Receipt
    fields = ['amount_paid','date_paid','comment']
    success_url = reverse_lazy('invoice-list')

    def form_valid(self,form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        obj.invoice = invoice
        obj.save()
        return redirect('invoice-list')

    def get_context_data(self,**kwargs):
        context = super(ReceiptCreateView,self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        context['invoice'] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin,UpdateView):
    model = Receipt
    fields = ['amount_paid','date_paid','comment']
    success_url = reverse_lazy('invoice-list')

class ReceiptDeleteView(LoginRequiredMixin,DeleteView):
    model = Receipt
    success_url = reverse_lazy('invoice-list')


@login_required
def bulk_invoice(request):
    students = Student.objects.all()
    initial = []
    for student in students:
        initial.append({'student':student,'class_for':student.current_class})
    if request.method =='POST':
        pass
    else:
        form = Invoices(initial=initial)

    return render(request,'finance/bulk_invoice.html',{'form':form})
