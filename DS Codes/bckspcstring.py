# Backspace string compare using stack

def backspaceCompare(S: str, T: str) -> bool:
    # Define a function that processes a string with backspaces
    def processString(S: str) -> str:
        # Initialize the stack
        stack = []

        # Iterate through the string
        for s in S:
            # If the character is a backspace, pop the top element from the stack
            if s == "#":
                if stack:
                    stack.pop()
            # If the character is not a backspace, push it onto the stack
            else:
                stack.append(s)

        # Return the processed string
        return "".join(stack)

    # Process the strings and compare the results
    return processString(S) == processString(T)


# Define the strings
S = "ab#c"
T = "ad#c"

# Compare the strings with backspaces
result = backspaceCompare(S, T)

# Print the result
print(result)
