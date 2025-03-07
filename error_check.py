class DatabaseError(Exception):
    """Exception raised for database-related errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ValidationError(Exception):
    """Exception raised for validation-related errors."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(self.message)

try:
    # Raising an ExceptionGroup with nested ExceptionGroups
    raise ExceptionGroup("Outer group", [
        ExceptionGroup("Inner group 1", [
            DatabaseError("DB Timeout"),
            ValidationError("email", "Invalid format")
        ]),
        ExceptionGroup("Inner group 2", [
            ValueError("An inner value error"),
            ValidationError("username", "Username is required")
        ])
    ])
except* DatabaseError as e:
    print("Handled DatabaseError")
except* ValidationError as e:
    print("Handled ValidationError:", [str(exc) for exc in e.exceptions])
except* ValueError:
    print("Handled ValueError")

def greet(name: str = "Guest", age: int = 30) -> 'str':
    return f"Hello {name}, you are {age} years old."

# Usage
print(greet())  # Uses default values
print(greet("Alice"))  # Overrides the default name
print(greet("Bob", 40))  # Overrides both default values


# Python program to print Fibonacci series 
def fib(n:'int', output:'list'=[])-> list: 
	if n == 0: 
		return output 
	else: 
		if len(output)< 2: 
			output.append(1) 
			fib(n-1, output) 
		else: 
			last = output[-1] 
			second_last = output[-2] 
			output.append(last + second_last) 
			fib(n-1, output) 
		return output 
print(fib(5)) 

def func(a,b=5,c=10):
    return a+b+c

print(func(3,c=6))

