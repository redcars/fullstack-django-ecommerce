from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .cart import Cart

from product.models import Product

def add_to_cart(request, product_id): 
    cart = Cart(request)
    cart.add(product_id)

    return render(request, 'cart/menu_cart.html')

def cart(request):
    return render(request, 'cart/cart.html')

def success(request):
    return render(request, 'cart/success.html')

def update_cart(request, product_id, action): 
    cart = Cart(request)

    if action == 'increment': # Funskjonalitet for å minske eller øke quantity til handlevogn produkter
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)
    
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    
    if quantity: # Fjerner produktet hvis det ikke er noe av 'quantity' variablen
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price),
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response

@login_required # Auth decorator som lar meg velge hvilke funskjoner som kan bli brukt bare av users som er logget inn
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE 
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

def hx_menu_cart(request):
    return render(request, 'cart/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')