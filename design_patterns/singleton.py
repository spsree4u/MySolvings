"""
Type: Creational
Name: Singleton
Creates only a single instance of the class.
1. Make constructor private
2. Add a static method which returns instance (static variable stores this instance). 
   Method will only creates an instance if it's already not created.
3. To make thread-safe, lock before the creation part inside static method and unlock after 
   creation, only for the first time
4. Make copy constructor and =operator overloading as private (in other languages)

Issues with Singleton:
1. Breaks object oriented design pattern as multiple instances can be created from multiple classes 
which are inherited from a singleton class
2. No control over creation of instance. Will not be able to know if the accessed instance is an already 
existing or new and hence
3. Testing code is difficult because we can't create a fresh instance for all instances
4. Don't work well with multi threaded application
"""

from threading import Lock, Thread

class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()
    # _lock = Lock()
    # print(_lock, Lock)

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # print(cls._instances)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    def log(self, msg):
        print(msg)

# logger = Logger()
# logger2 = Logger()
# print(logger)
# print(logger2)
# logger.log("Hello")
# logger2.log("Hi")

def threaded_logger(msg):
    logger = Logger()
    print(logger)
    logger.log(msg)

process1 = Thread(target=threaded_logger, args=("Hello Thread 1",))
process2 = Thread(target=threaded_logger, args=("Hello Thread 2",))
process3 = Thread(target=threaded_logger, args=("Hello Thread 3",))
process1.start()
process2.start()
process3.start()
