from products.models import Product


class InCartException(Exception):
    pass


class UnAvailabeProduct(Exception):
    pass


class OutOffCart(Exception):
    pass


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = request.session.get("cart")
        if not cart:
            cart = request.session["cart"] = {}
        self.cart = cart


    def increase(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            if product.inventory > self.cart.get(product_id).get("quantity"):
                self.cart[product_id]["quantity"] += 1
                self.save()
            else:
                raise UnAvailabeProduct()

    def add(self, product, color_obj = None):
        product_id = str(product.pk)
        if product.inventory > 0:
            if not product_id in self.cart.keys():
                product_price = product.price_after_off if product.off else product.price
                self.cart[product_id] = {
                    "quantity": 1, "price": product_price, "name": product.name, "weight": product.weight, "color" : {"id" : color_obj.pk,"name" : color_obj.name, "style_color_class": color_obj.style_class} if color_obj else None}
                self.save()
            else:
                raise InCartException()
        else:
            raise UnAvailabeProduct()

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            if self.cart[product_id]["quantity"] == 1:
                self.remove(product)
                self.save()
                raise OutOffCart()

            else:
                self.cart[product_id]["quantity"] -= 1
                self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()

    def item_count(self):
        return len(self.cart.keys())

    def __iter__(self):
        products = {str(p.id): p for p in Product.objects.filter(
            pk__in=self.cart.keys()).distinct()}
        for product_id, item in self.cart.items():
            item_copy = item.copy()
            item_copy["product"] = products.get(product_id)
            item_copy["product_total_price"] = item_copy["quantity"] * \
                item_copy["price"]
            yield item_copy

    def total_items(self):
        return sum(item["quantity"] for item in self.cart.values())

    def total_price(self):
        return sum(item["quantity"] * item["price"] for item in self.cart.values())

    def total_weight(self):
        return sum(item["quantity"] * item["weight"] for item in self.cart.values())

    def post_price(self):
        total_weight = self.total_weight()
        if total_weight >= 1000:
            return 100000
        if total_weight < 1000:
            return 50000
        

    def total_price(self):
        return sum(item["quantity"] * item["price"] for item in self.cart.values())

    def final_price(self):
        return self.total_price() + self.post_price()

    def save(self):
        self.session.modified = True
