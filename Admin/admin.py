# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Transaction


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'phone_number', 'city', 'date_joined', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'city', 'country')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'phone_number', 'city', 'country', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'brand', 'category')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand', 'category', 'description')
    list_editable = ('price', 'quantity')  
    ordering = ('-id',)
    prepopulated_fields = {"brand": (), "category": ()} 


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_reference_number', 'customer_name', 'customer_phone_number',
                    'transaction_amount', 'transaction_method', 'transaction_status', 'transaction_date')
    list_filter = ('transaction_status', 'transaction_method', 'transaction_date')
    search_fields = ('customer_name', 'customer_phone_number', 'transaction_reference_number', 'transaction_code')
    readonly_fields = ('transaction_date', 'transaction_reference_number', 'transaction_code')
    ordering = ('-transaction_date',)

    list_editable = ('transaction_status',)

    fieldsets = (
        ('Customer', {
            'fields': ('customer_name', 'customer_phone_number')
        }),
        ('Payment Details', {
            'fields': ('transaction_amount', 'transaction_method', 'transaction_status')
        }),
        ('System Info', {
            'fields': ('transaction_reference_number', 'transaction_code',
                       'transaction_result_description', 'transaction_date'),
            'classes': ('collapse',)  # Collapsed by default
        }),
    )