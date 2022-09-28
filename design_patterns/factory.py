

class Product(object):
    name = ""

    def get_product(self):
        return self.name

class P1(Product):
    name = "Product 1"
    
class P2(Product):
    name = "Product 2"

class ProductFactory:

    def create_product(self, prod_type):
        prod_type = prod_type.capitalize()
        return globals()[prod_type]()

if __name__ == '__main__':
    prod_factory_obj = ProductFactory()
    print(prod_factory_obj.create_product('p1').get_product())
    print(prod_factory_obj.create_product('p2').get_product())
