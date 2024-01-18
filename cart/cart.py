from django.conf import settings

from product.models import Product

class Cart(object): # Initialiserer handlevogn i et session, lar meg også manipulerer handlevogns innholdet
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self): # Sjekker igjennom handlevogns produktenene, fetcher informasjon og total prisen basert på kvantiteten
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity'])

            yield item

    def __len__(self): # Summerer mengden av produkter i handlevognen
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self): # Lar meg oppdatere session data med innholdet av handlevognen, og putter på et "modified" flagg for å vise at sessionen har blitt modifisert.
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False): # Lar meg legge til, fjerne og endre mengen av et produkt i handlevognen
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()

    def remove(self, product_id): # Funksjon for å fjerne et produkt fra handlevognen
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self): # Clearer hele vognen, ved å fjerne sessionet
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self): # Returnerer total kosten i handlevognen
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['product'].price * item['quantity'] for item in self.cart.values())
    
    def get_item(self, product_id): # Funksjon for å få produkt i return
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None
            

