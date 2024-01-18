from .cart import Cart

def cart(request): # Returnerer et dictionary med info fra handlevognen
    return {'cart': Cart(request)}