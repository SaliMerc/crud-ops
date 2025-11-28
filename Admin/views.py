from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product

def admin(request):
    product=Product.objects.all()
    context={'products':product}
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