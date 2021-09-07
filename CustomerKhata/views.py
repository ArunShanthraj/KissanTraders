import os
import random
import qrcode

from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from itertools import chain
from .models import *
from .forms import CreateUserForm, TransactionForm, AddCustomerForm
from .filters import TransactionFilters, CustomerFilters
from datetime import datetime
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

'''def validation_required(func):

    def wrapper(*args, **kwargs):
        print(str(args))
        # if request.POST.get("otp_status"):
        if func(*args, **kwargs):
            return HttpResponse('you are not valid user to view this page')

    return wrapper
'''


def link_callback(uri, rel):
    STATIC_ROOT = r'H:\PyCharmProjects\KissanTraders\static'
    path = os.path.join(STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all().values()
        all_customers_transaction = CustomerTransaction.objects.all().values('customer').annotate(
            gisum=Sum('AmountGiven'), gosum=Sum('AmountGot'), eachbalance=F('gisum') - F('gosum'))
        totalAmount = sum(all_customers_transaction.values_list('eachbalance', flat=True))
        transaction_dict = {d['customer']: d for d in all_customers_transaction}

        for d in customers:
            if d['id'] not in transaction_dict.keys():
                transaction_dict[d['id']] = {'customer': d['id'], 'gisum': 0, 'gosum': 0, 'eachbalance': 0}
            transaction_dict[d['id']].update(d)

        data = {
            "company": "Kissan Traders",
            "address": "B.H.Road, Kargal",
            "city": "sagara",
            "district": "Shimogga",
            "State": "KA",
            "zipcode": "577421",
            "transaction_dicts": transaction_dict.values(),
            "phone_num": "+919480262244",
            "email": "kissankargal@gmail.com",
            "totalAmount": totalAmount,
            "header_tag": "Customer Details"
        }
        pdf = render_to_pdf('CustomerKhata/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automatically downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all().values()
        all_customers_transaction = CustomerTransaction.objects.all().values('customer').annotate(
            gisum=Sum('AmountGiven'), gosum=Sum('AmountGot'), eachbalance=F('gisum') - F('gosum'))
        totalAmount = sum(all_customers_transaction.values_list('eachbalance', flat=True))
        transaction_dict = {d['customer']: d for d in all_customers_transaction}

        for d in customers:
            if d['id'] not in transaction_dict.keys():
                transaction_dict[d['id']] = {'customer': d['id'], 'gisum': 0, 'gosum': 0, 'eachbalance': 0}
            transaction_dict[d['id']].update(d)

        data = {
            "company": "Kissan Traders",
            "address": "B.H.Road, Kargal",
            "city": "sagara",
            "district": "Shimogga",
            "State": "KA",
            "zipcode": "577421",
            "transaction_dicts": transaction_dict.values(),
            "phone_num": "+919480262244",
            "email": "kissankargal@gmail.com",
            "totalAmount": totalAmount,
            "header_tag": "Customer Details"
        }

        now = datetime.now()
        vdatetime = now.strftime("%d_%m_%Y_%H_%M_%S")

        pdf = render_to_pdf('CustomerKhata/pdf_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Customer_Details_%s.pdf' % (vdatetime)
        content = 'attachment; filename= %s' % (filename)
        response['Content-Disposition'] = content
        return response


# Opens up page as PDF
class ViewtransactionPDF(View):
    def get(self, request, *args, **kwargs):
        selectedcustomer = Customer.objects.get(id=self.kwargs['pk'])
        selected_customertransaction = CustomerTransaction.objects.filter(customer=selectedcustomer)
        TotalAmountGiven = sum(selected_customertransaction.values_list('AmountGiven', flat=True))
        TotalAmountGot = sum(selected_customertransaction.values_list('AmountGot', flat=True))
        totalAmount = TotalAmountGiven - TotalAmountGot

        data = {
            "company": "Kissan Traders",
            "address": "B.H.Road, Kargal",
            "city": "sagara",
            "district": "Shimogga",
            "State": "KA",
            "zipcode": "577421",
            "transaction_dicts": selected_customertransaction,
            "phone_num": "+919480262244",
            "email": "kissankargal@gmail.com",
            "totalAmount": totalAmount,
            "header_tag": "Transaction Details"
        }
        pdf = render_to_pdf('CustomerKhata/transaction_pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automatically downloads to PDF file
class DownloadtransactionPDF(View):
    def get(self, request, *args, **kwargs):
        selectedcustomer = Customer.objects.get(id=self.kwargs['pk'])
        selected_customertransaction = CustomerTransaction.objects.filter(customer=selectedcustomer)
        TotalAmountGiven = sum(selected_customertransaction.values_list('AmountGiven', flat=True))
        TotalAmountGot = sum(selected_customertransaction.values_list('AmountGot', flat=True))
        totalAmount = TotalAmountGiven - TotalAmountGot

        data = {
            "company": "Kissan Traders",
            "address": "B.H.Road, Kargal",
            "city": "sagara",
            "district": "Shimogga",
            "State": "KA",
            "zipcode": "577421",
            "transaction_dicts": selected_customertransaction,
            "phone_num": "+919480262244",
            "email": "kissankargal@gmail.com",
            "totalAmount": totalAmount,
            "header_tag": "Transaction Details"
        }

        now = datetime.now()
        vdatetime = now.strftime("%d_%m_%Y_%H_%M_%S")

        pdf = render_to_pdf('CustomerKhata/transaction_pdf_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Transaction_Details_%s.pdf' % (vdatetime)
        content = 'attachment; filename= %s' % (filename)
        response['Content-Disposition'] = content
        return response


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'CustomerKhata/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('validate_otp')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                rno = random.randint(100000, 999999)
                global otp
                otp = rno
                im = qrcode.make("OTP :" + str(rno))
                im.save(r"./static/images/qrimages.png")
                return render(request, 'CustomerKhata/qrcode_page.html')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'CustomerKhata/login.html', context)


@login_required(login_url='login')
def validateOTP(request):
    user_otp = request.POST.get("otp")
    if user_otp == str(otp):
        return redirect('home')
    else:
        messages.error(request, "INVALID OTP ENTERED")
        return render(request, 'CustomerKhata/qrcode_page.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all().values()
    total_customers = customers.count()
    transactiondata = CustomerTransaction.objects.all().order_by('-transaction_date')[:10]
    groupeddata = CustomerTransaction.objects.all().values('customer').annotate(gisum=Sum('AmountGiven'),
                                                                                gosum=Sum('AmountGot'),
                                                                                givenamount=F('gisum') - F('gosum'),
                                                                                gotamount=F('gosum') - F('gisum'))
    TotalAmountGiven = sum(groupeddata.values_list('givenamount', flat=True))
    TotalAmountGot = sum(groupeddata.values_list('gotamount', flat=True))

    myFilter = CustomerFilters(request.GET, queryset=customers)
    customers = myFilter.qs

    if TotalAmountGiven < 0:
        TotalAmountGiven = 0

    if TotalAmountGot < 0:
        TotalAmountGot = 0

    context = {'customers': customers, 'transactions': transactiondata, 'total_customers': total_customers,
               'yougive': TotalAmountGot, 'youget': TotalAmountGiven, 'myFilter': myFilter}
    return render(request, 'CustomerKhata/dashboard.html', context)


@login_required(login_url='login')
def Add_Customer(request):
    form = AddCustomerForm()
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            customer = form.cleaned_data.get('name')

    context = {'form': form}
    return render(request, 'CustomerKhata/add_customer.html', context)


@login_required(login_url='login')
def Add_Customer_form_submission(request):
    customer_name = request.POST['name']
    customer_phone = request.POST['phone']

    for instance in Customer.objects.all():
        if instance.name == customer_name:
            messages.error(request, 'There is an existing customer with the name:' + customer_name)
            return redirect('add_customer')

        elif instance.phone == customer_phone:
            messages.error(request, 'There is an existing customer with the phone:' + customer_phone)
            return redirect('add_customer')

    customer_info = Customer(name=customer_name, phone=customer_phone)
    customer_info.save()
    messages.success(request, 'Added Customer :' + customer_name)
    return redirect('home')


@login_required(login_url='login')
def customer(request, pk):
    selectedcustomer = Customer.objects.get(id=pk)
    selected_customertransaction = CustomerTransaction.objects.filter(customer=selectedcustomer)
    TotalAmountGiven = sum(selected_customertransaction.values_list('AmountGiven', flat=True))
    TotalAmountGot = sum(selected_customertransaction.values_list('AmountGot', flat=True))

    myFilter = TransactionFilters(request.GET, queryset=selected_customertransaction)
    selected_customertransaction = myFilter.qs

    label = ""
    balance = 0
    if TotalAmountGiven > TotalAmountGot:
        label = "You Will Get"
        balance = TotalAmountGiven - TotalAmountGot
    elif TotalAmountGiven < TotalAmountGot:
        label = "You Will Give"
        balance = TotalAmountGot - TotalAmountGiven
    else:
        label = "balance"
        balance = 0
    context = {'customer': selectedcustomer, 'transactions': selected_customertransaction, 'labeltext': label,
               'balancetext': balance, 'myFilter': myFilter}
    return render(request, 'CustomerKhata/customer.html', context)


@login_required(login_url='login')
def add_transaction(request, pk):
    transactionformset = inlineformset_factory(Customer, CustomerTransaction, fields=('AmountGiven', 'AmountGot'),
                                               extra=1, can_delete=False, validate_min=1)
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        formset = transactionformset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('customer', pk=customer.id)

    formset = transactionformset(instance=customer)
    context = {'form': formset, 'customer': customer}
    return render(request, 'CustomerKhata/add_transaction.html', context)
