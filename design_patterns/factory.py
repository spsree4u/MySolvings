
'''
Type: Creational
Name: Factory
Use: Creates objects of different sub-classes (using base class type in type-based languages like Java, C++, etc) 
without providing the details of class implementations to the client/user. 
For a user, just some parameter which represent the class (for which the object is returned) is required and 
using this object user can access the class attributes.
'''

class Product(object):
    name = ""

    def get_product(self):
        return self.name

class P1(Product):
    name = "Product 1"
    
class P2(Product):
    name = "Product 2"

class ProductFactory:

    # Factory method which returns the class object on providing class name or some class identifier
    def create_product(self, prod_type):
        prod_type = prod_type.capitalize()
        return globals()[prod_type]()

if __name__ == '__main__':
    prod_factory_obj = ProductFactory()
    print(prod_factory_obj.create_product('p1').get_product())
    print(prod_factory_obj.create_product('p2').get_product())
