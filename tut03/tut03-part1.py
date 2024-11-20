n = int(input("Enter the number: "))
a = len(str(n))
b = str(n)

rotations = []
rotations.append(n)
for i in range(1, a):
    r = b[i:] + b[:i]
    rotations.append(int(r))
print(rotations)

flag = True
for x in rotations:
    if x < 2:
        print(f"{x} is not a prime number")
        flag = False
        break
    for j in range(2, int(x**0.5) + 1):
        if x % j == 0:
            print(f"{x} is not a prime number")
            flag = False
            break
    if not flag:
        break

if flag:
    if a==2:
        print(f"Both are Rotational primes")
    elif a>2:
       print(f"All are Rotational primes")

    print(f"{n} is a Rotational prime.")
else:
    print(f"{n} is not a Rotational prime.")
rotations
a