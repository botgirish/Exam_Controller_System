s = input("Enter string: ")
b= len(s)
st= ""
count=1
for i in range(1,b):

    if s[i] == s[i-1]:
      count += 1
    else:
      st += s[i-1] + str(count)
      count= 1
st += s[-1] + str(count)

print(st)