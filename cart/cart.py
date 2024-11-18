from store.models import Product


#------------------------------------------------------------------
# To manage shopping cart with session :
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qyt'] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        import copy
        # cart = self.cart.copy()
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
        self.session.modified = True

    def get_total_cart_price(self):
        return sum(int(item['price']) * item['qty'] for item in self.cart.values())
