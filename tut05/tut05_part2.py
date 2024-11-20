string = input("Enter the string: ")
n = len(string)

s = ""
for char in string:
    s = char + s

ns = ""
for i in range(n):
    if string[i] == '(':
        ns += ')'
    elif string[i] == ')':
        ns += '('
    elif string[i] == '{':
        ns += '}'
    elif string[i] == '}':
        ns += '{'
    elif string[i] == '[':
        ns += ']'
    elif string[i] == ']':
        ns += '['
    else:
        ns += string[i]

if s == ns:
    print("The input string is Balanced")
else:
    print("The input string is NOT balanced")


