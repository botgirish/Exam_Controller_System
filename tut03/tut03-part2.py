#lab3 q2
def generate_permutations(string):
    # Convert the string into a list of characters
    chars = list(string)
    n = len(chars)

    # Create an array to control the indices
    indices = list(range(n))

    # Sort characters to generate permutations in lexicographic order
    chars.sort()

    # Flag to indicate when all permutations are completed
    done = False

    print(f"Permutations of '{string}':")

    while not done:
        # Print the current permutation
        print(''.join(chars))

        # Find the rightmost index (i) where chars[i] < chars[i + 1]
        i = n - 2
        while i >= 0 and chars[i] >= chars[i + 1]:
            i -= 1

        if i < 0:
            done = True
        else:
            # Find the smallest character to the right of i that is larger than chars[i]
            j = n - 1
            while chars[j] <= chars[i]:
                j -= 1

            # Swap characters at i and j
            chars[i], chars[j] = chars[j], chars[i]

            # Reverse the sequence to the right of i
            chars = chars[:i + 1] + chars[i + 1:][::-1]

# Get input from the user
user_input = input("Enter a string to generate its permutations: ")
generate_permutations(user_input)