
'''
    - Number Encoder
        You can import string or use the below ascii_lowercase 
'''


from string import ascii_lowercase
# ascii_lowercase ='abcdefghijklmnopqrstuvwxyz'
def main(n):
    try:
        count2 = 1
        dct1 = {}
        for i in ascii_lowercase:
            dct1[i] = count2
            count2+=1
        str = ''
        for j in range(len(ascii_lowercase)):
            for k in range(len(ascii_lowercase)):
                str = ascii_lowercase[j]+ascii_lowercase[k]
                dct1[str] = count2
                count2 += 1
        for key1, vl in dct1.items():
            if vl == int(n):
                print(key1.upper())
                return key1.upper()
        if int(n)<0 or int(n)>len(dct1):
            raise Exception
    except ValueError:
        print("Enter values without decimal")
    except Exception as e:
        print("Enter positive value within small range",e)


print("Enter positive number:")
n = str(input())
main(n)