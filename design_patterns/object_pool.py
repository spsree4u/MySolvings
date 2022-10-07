"""
Type: Creational
Name: Object Pool
Reusable pool of fixed number of instances will be always readily available for to use.
Use case 1: Object creation is expensive, but need objects for short time. 
Ex: DB connection, Graphics objects containing a lot of mesh data that are drawn over and over again.

Limitations:
1. We can still create instances outside of the object pool
2. Can write code that uses an instance after it is released. NOTE: Meta classes can be used for more restrictions.
3. Make sure set the object back to fresh state when releases it
4. Multi threading issue of accessing same object by multi threads
"""

class Reusable:

    def show_instance(self):
        print(f"Using instance {id(self)}")

class ReusablePool:

    def __init__(self, size):
        self.size = size
        self.free_instances = []
        self.in_use_instances = []
        for _ in range(size):
            self.free_instances.append(Reusable())

    def hold(self):
        if not self.free_instances:
            raise Exception("No more instances are available")

        i = self.free_instances[0]
        self.free_instances.remove(i)
        self.in_use_instances.append(i)
        return i

    def release(self, i):
        self.in_use_instances.remove(i)
        self.free_instances.append(i)


# pool = ReusablePool(2)
# i1 = pool.hold()
# i2 = pool.hold()
# i1.show_instance()
# i2.show_instance()
# pool.release(i2)
# # i2.show_instance()
# i3 = pool.hold()
# i3.show_instance()

# This can be improved by using a context manager class
class PoolManager:

    def __init__(self, pool):
        self.pool = pool

    def __enter__(self):
        self.instance = self.pool.hold()
        return self.instance

    def __exit__(self, type, value, traceback):
        self.pool.release(self.instance)

pool = ReusablePool(2)
with PoolManager(pool) as i:
    i.show_instance()

with PoolManager(pool) as i:
    i.show_instance()

with PoolManager(pool) as i:
    i.show_instance()
