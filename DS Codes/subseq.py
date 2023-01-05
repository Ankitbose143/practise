# To determine whether one string is a subsequence of another string in Python, you can use a loop to iterate through the characters of the longer string and check if they match the characters of the shorter string in order.

def is_subsequence(s, t):
    # Keep track of the current position in s
    i = 0

    # Iterate through the characters in t
    for c in t:
        # If c matches the current character in s, move to the next character in s
        if i < len(s) and s[i] == c:
            i += 1

    # Return True if we have reached the end of s, False otherwise
    return i == len(s)

# This function takes in two strings s and t and returns a boolean indicating whether s is a subsequence of t or not.

result = is_subsequence("abc", "abcd")
print(result)  # prints True

result = is_subsequence("abc", "acd")
print(result)  # prints False
