import time
import functools

def retry(max_retries=3, delay=1):
    """Decorator to retry a function if it fails, with a delay between retries."""
    def decorator(func):
        #@functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f"Attempt {retries}/{max_retries} failed: {e}")
                    if retries < max_retries:
                        time.sleep(delay)  # Wait before retrying
                    else:
                        print("Max retries reached. Raising exception.")
                        raise
        return wrapper
    return decorator



import random

@retry(max_retries=8, delay=2)  # Retries up to 5 times with a 2-second delay
def risky_function():
    """Simulates a function that fails randomly."""
    if random.random() < 0.75:  # 70% chance of failure
        print(random.random())
        raise ValueError("Random failure occurred")
    return "Success!"

# Run the function
print(risky_function())

#double decorator
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("Decorator 1")
        func(*args, **kwargs)
        print("Decorator 12")
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("Decorator 2")
        func(*args, **kwargs)
        print("Decorator 21")
    return wrapper

@decorator1
@decorator2
def my_function():
    print("Hello from my_function")

my_function()


def mydec(f):
    def wrapper(*args):
        print("any",any(int(arg) < 0 for arg in args), all(int(arg) < 0 for arg in args))
        print("all", type(any(int(arg) < 0 for arg in args)))
        if any(int(arg) < 0 for arg in args):
            # if int(i)<0 or int(i)<0:
            sum_np = "sum not possible"
            # f(*args)	
        else:
            sum_np = "sum possible"
            f(*args)
        return sum_np
    return wrapper


@mydec
def add(a,b):
    sum = a+b
    print("sum",sum)
    return sum

print(add(5,2))