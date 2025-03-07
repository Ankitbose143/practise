from collections import Counter

def smallest_substring(s, pattern):
    char_count = Counter(pattern)
    print("counter", char_count)
    left = 0
    min_length = float('inf')
    min_substring = ""
    required_chars = len(pattern)
    print("min_length",min_length)
    for right in range(len(s)):
        # print("sright",s[right], char_count)
        if s[right] in char_count:
            if char_count[s[right]] > 0:
                required_chars -= 1
            char_count[s[right]] -= 1
            print(char_count[s[right]])

        while required_chars == 0:
            print("min_length12",s[:right],right, left, min_length)
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_substring = s[left:right+1]

            if s[left] in char_count:
                char_count[s[left]] += 1
                if char_count[s[left]] > 0:
                    required_chars += 1

            left += 1

    return min_substring

# Example cases
print(smallest_substring("i am the greatest", "imt"))  # Output: "i am t"
print(smallest_substring("My name is Fran", "rim"))    # Output: "me is Fr"
