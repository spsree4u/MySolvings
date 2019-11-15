
# Sort characters in a word


# O(n) time and O(1) space
def word_sort(s):
    char_count = [0 for _ in range(26)]
    for i in s:
        char_count[ord(i) - ord('a')] += 1

    for i in range(26):
        for j in range(char_count[i]):
            print(chr(i + ord('a')))


word_sort("helloworld")
