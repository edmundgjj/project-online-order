from django.shortcuts import render
from .models import Menu
from cart.models import CartItem


# Create your views here.
def menu(request):
    all_products = Menu.objects.all()
    all_cart_items = CartItem.objects.all()
    
    return render(request, 'menu/menu_items.template.html', {
        'all_products': all_products,
        'all_cart_items': all_cart_items
    })
