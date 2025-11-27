from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# Create your views here.
def admin(request):
    product=Product.objects.all()

    # Search Functionality: By product name
    search_query = request.GET.get('search')
    if search_query:
        product = product.filter(name__icontains=search_query)

    context={'products':product}
    return render(request, 'admin.html', context)

def add_item(request):
    if request.method == 'POST':
        # Process the form data here
        try:
            name=request.POST.get('name')
            price=request.POST.get('price')
            description=request.POST.get('description')
            
            brand=request.POST.get('brand')
            category=request.POST.get('category')
            quantity=request.POST.get('quantity')
            
            Product.objects.create(
                name=name,
                price=price,
                description=description,
                brand=brand,
                category=category,
                quantity=quantity
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
    
    
    return render (request, 'update_item.html', context)

"""
Please update your Product model by adding the following three fields: 
brand, category (Take input from user, no dropdown), and quantity.
After updating the model, ensure that each of these new fields is displayed correctly in your products table on the dashboard.
"""