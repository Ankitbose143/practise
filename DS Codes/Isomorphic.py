# to map the characters in one string to the corresponding characters in the other string.
def is_isomorphic(s, t):
    # Initialize the mapping dictionary
    mapping = {}

    # Zip the two strings and iterate over the pairs of characters
    for c1, c2 in zip(s, t):
        print(c1,c2)
        # If c1 has not been mapped yet, map it to c2
        if c1 not in mapping:
            mapping[c1] = c2
            print("mapping if", mapping)
        # If c1 has already been mapped, check that it is mapped to c2
        elif mapping[c1] != c2:
            print("mapping else", mapping)
            return False

    # Check that each character in t is mapped to a unique character in s
    values = set(mapping.values())
    if len(values) != len(mapping):
        return False

    return True


# This function takes in two strings s and t and returns a boolean indicating whether they are isomorphic or not.
#
# To use this function, you would pass in the two strings as arguments. For example:



result = is_isomorphic("foo", "bar")
print(result)  # prints True

result = is_isomorphic("foo", "baz")
print(result)  # prints False
