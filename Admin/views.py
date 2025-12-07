from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Transaction, CustomUser
from django.db import IntegrityError

from django_daraja.mpesa.core import MpesaClient
from django.conf import settings

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from Admin.permissions import role_permission_required
from django.contrib.auth import authenticate, login, logout

from Admin.roles import DriverRole
from rolepermissions.roles import assign_role

def admin(request):
    products=Product.objects.all()
    
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query)
        )
    context={
        'products':products,
        'query':query
        }
    return render(request, 'admin.html', context)

def add_item(request):
    if request.method == 'POST':
        try:
            name=request.POST.get('name')
            price=request.POST.get('price')
            description=request.POST.get('description')
            
            brand=request.POST.get('brand')
            category=request.POST.get('category')
            quantity=request.POST.get('quantity')
            
            image=request.FILES.get('image')
            
            Product.objects.create(
                name=name,
                price=price,
                description=description,
                brand=brand,
                category=category,
                quantity=quantity,
                image=image
            )
            return redirect('admin')
        except Exception as e:
            print(e)
    return render(request, 'add_item.html')

def delete(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin')

def update_item(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    context={'product':product}
    
    if request.method == 'POST':
        try:
            product.name=request.POST.get('name')
            product.price=request.POST.get('price')
            product.description=request.POST.get('description')
            
            product.brand=request.POST.get('brand')
            product.category=request.POST.get('category')
            product.quantity=request.POST.get('quantity')
            
            if 'image' in request.FILES:
                product.image=request.FILES.get('image')
            
            product.save()
            return redirect('admin')
        except Exception as e:
            print(e)    
    
    return render (request, 'update_item.html', context)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        country = request.POST.get('country')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([first_name, last_name, phone_number, email, password, confirm_password]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')   

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, 'signup.html')   

        try:
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                city=city,
                country=country,
                role = 'driver',
            )
            assign_role(user, DriverRole)
            print("User created successfully:", user.email)

            messages.success(request, f"Welcome, {first_name}! Your account has been created.")
            return redirect('login')

        except Exception as e:
            print("Error creating user:", e)
            messages.error(request, "Account creation failed. Please try again.")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def login_view(request):   
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)   

            if user.role == 'driver':  
                return redirect('payments_made')
            return redirect('')

        messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
@role_permission_required('see_assigned_bins')
def payments_made(request):
    transactions=Transaction.objects.all()
    
    query = request.GET.get('q')
    if query:
        transactions = transactions.filter(
            Q(customer_name__icontains=query) | 
            Q(transaction_status__icontains=query) |
            Q(transaction_code__icontains=query) |
            Q(customer_phone_number__icontains=query)
        )
    context={
        'transactions':transactions,
        'query':query
        }
    return render(request, 'payments_made.html', context)
    

def mpesa_payment(request):
    if request.method == 'POST':
        try:
            customer_name=request.POST.get('customer_name')
            customer_phone_number=request.POST.get('customer_phone_number')
            transaction_amount=int(request.POST.get('transaction_amount'))
            
            mpesa_client = MpesaClient()
            
            account_reference = settings.MPESA_ACCOUNT_REFERENCE
            transaction_desc = settings.MPESA_TRANSACTION_DESC
            callback_url = settings.MPESA_CALLBACK_URL
            response = mpesa_client.stk_push(
                customer_phone_number, 
                transaction_amount, 
                account_reference, 
                transaction_desc, 
                callback_url
            )
            
            response_data = response.json()
            if response.status_code == 200:
                checkout_request_id = response_data.get('CheckoutRequestID')
                customer_message = response_data.get('CustomerMessage')

                Transaction.objects.create(
                    customer_name=customer_name,
                    customer_phone_number=customer_phone_number,
                    transaction_amount=transaction_amount,
                    transaction_method='mpesa',
                    transaction_result_description= customer_message,
                    transaction_reference_number=checkout_request_id,
                    transaction_status='pending',
                    transaction_code='N/A'
                )
                print("M-Pesa STK Push initiated successfully.")
            else:
                print("Failed to initiate M-Pesa STK Push.")
        except Exception as e:
            print(e)
    return render(request, 'mpesa_payment.html')


@csrf_exempt
def mpesa_callback(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)

        stk_callback = data["Body"]["stkCallback"]
        result_code = stk_callback["ResultCode"]
        checkout_request_id = stk_callback["CheckoutRequestID"]

        """Find the pending transaction"""
        try:
            transaction = Transaction.objects.get(
                transaction_reference_number=checkout_request_id,
                transaction_status='pending'
            )
        except Transaction.DoesNotExist:
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

        """If a transaction is not successfull"""
        if result_code != 0:
            result_desc = stk_callback.get("ResultDesc")
            transaction.transaction_status = 'failed'
            transaction.transaction_result_description = result_desc
            transaction.save()

            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

        """If transaction is successfull"""
        result_desc = stk_callback.get("ResultDesc")
        items = stk_callback["CallbackMetadata"]["Item"]  

        mpesa_code = next((item["Value"] for item in items if item["Name"] == "MpesaReceiptNumber"), None)
        phone_number = next((item["Value"] for item in items if item["Name"] == "PhoneNumber"), None)
        amount = next((item["Value"] for item in items if item["Name"] == "Amount"), 0)

        """Update the Transaction table"""
        transaction.transaction_amount = amount
        transaction.transaction_code = mpesa_code 
        transaction.customer_phone_number = str(phone_number)
        transaction.transaction_status = 'completed'
        transaction.transaction_result_description = result_desc
        transaction.save()
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print("M-Pesa Callback Error:", str(e))
        print("Raw payload:", request.body.decode('utf-8', errors='ignore'))
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})



