from collections import defaultdict, Counter

def anagram_groups(words):
    anagram_dict = defaultdict(list)

    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_dict[sorted_word].append(word)

    return anagram_dict

def calculate_freq(anagram_dict):
    frequency_dict = {}

    for sorted_word, anagram_group in anagram_dict.items():
        total_frequency = Counter()
        for word in anagram_group:
            total_frequency += Counter(word)
        frequency_dict[sorted_word] = dict(total_frequency)

    return frequency_dict

def highest_grp_freq(frequency_dict):
    max_frequency = 0
    max_frequency_group = None

    for group, frequencies in frequency_dict.items():
        total_frequency = sum(frequencies.values())
        if total_frequency > max_frequency:
            max_frequency = total_frequency
            max_frequency_group = group

    return max_frequency_group, max_frequency

#words = ["listen", "silent", "enlist", "inlets", "google", "goolge", "cat", "tac", "act"]
words = list(input("Enter the list of words separated by spaces: ").split())

anagram_dict = anagram_groups(words)

frequency_dict = calculate_freq(anagram_dict)

max_group, max_freq = highest_grp_freq(frequency_dict)

print("Input Words :", words)
print("Anagram Dictionary:", anagram_dict)
print("Character Frequency Dictionary:", frequency_dict)
print(f"Group with highest frequency: '{max_group}' with frequency {max_freq}")
