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
"""

from threading import Lock, Thread

class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
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
process1.start()
process2.start()
