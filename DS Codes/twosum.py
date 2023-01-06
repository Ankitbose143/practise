# two sum hashmap
def twoSum(nums: list[int], target: int) -> list[int]:
    # Initialize the hash map
    hash_map = {}

    # Iterate through the list
    for i, num in enumerate(nums):
        # Calculate the complement of the current element
        complement = target - num
        # Check if the complement is in the hash map
        if complement in hash_map:
            # If it is, return the indices of the two elements
            return [hash_map[complement], i]
        # If it isn't, add the current element to the hash map
        hash_map[num] = i

    # If no two elements sum to the target, return an empty list
    return []

# Define the list and target value
nums = [2, 7, 11, 15]
target = 9

# Find the two elements that sum to the target
result = twoSum(nums, target)

# Print the result
print(result)
