class add:
	def sum(self):
		print("hi sum")
		#return 
	
class overwrite(add):	
	def sum(self,a,b):
		return a+b
	
# obj = add()
obj = overwrite()
print(obj.sum(5,9))

f = (y for y in range(100))
print(next(f), type(f))
print(next(f))
print(next(f))
print(next(f))

def appealSum(s: str) -> int:
    last_pos = {}  # Stores the last occurrence of each character
    total_appeal = 0
    current_appeal = 0  # Appeal sum for substrings ending at i

    for i, ch in enumerate(s):
        # Calculate contribution of the character at index i
        print("ch", ch)
        if ch in last_pos:
            current_appeal += (i - last_pos[ch])
            print("current_appeal1", current_appeal)
            print("last_pos", last_pos, last_pos[ch])
        else:
            current_appeal += (i + 1)  # First occurrence contributes to all substrings from 0 to i
            print("current_appeal12", current_appeal)
            print("last_pos", last_pos)
        
        # Update last seen position of ch
        last_pos[ch] = i

        # Add to total appeal
        total_appeal += current_appeal

    return total_appeal


print(appealSum("abbca"))

print(appealSum("code"))