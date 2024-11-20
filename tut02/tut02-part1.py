n = int(input("Enter Number: "))
b= len(str(n))

while n>=10:
    sum = 0
    for i in range(b):
        a= n%10
        sum += a
        n = n//10
    n = sum

print(n)
