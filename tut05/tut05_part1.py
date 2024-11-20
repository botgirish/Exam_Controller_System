input_str = input("Enter a list of numbers separated by spaces: ")
nums = list(map(int, input_str.split()))

def find_triplets(nums):
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

    triplets = set()

    for i in range(len(nums) - 2):
        seen = set()
        for j in range(i + 1, len(nums)):
            complement = -nums[i] - nums[j]
            if complement in seen:
                triplets.add((nums[i], complement, nums[j]))
            seen.add(nums[j])

    return [list(triplet) for triplet in triplets]

triplets = find_triplets(nums)
print(triplets)


