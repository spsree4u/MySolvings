

def word_count(s):
    index = 0
    wc = 0
    in_word = True
    length = len(s)

    while s[index] == ' ' and index < length - 1:
        index += 1

    if index == length - 1:
        return "String with only spaces"

    while index <= length - 1:
        if s[index] == ' ':
            while s[index] == ' ' and index < length - 1:
                index += 1
            in_word = False
            wc += 1
        else:
            in_word = True
        index += 1

    if in_word:
        wc += 1

    return wc


print(word_count(" Ben ate  hay "))
print(word_count("  "))


def repeated_word_count(s):
    unique = set()
    words = s.split()
    for w in words:
        if w not in unique:
            unique.add(w)

    return len(words) - len(unique)


print(repeated_word_count("hello i am sreejith i hi hello am i "))


def first_match(s1, s2):
    """
    Determining the first matching character between two strings
    """
    for i in range(len(s1)):
        while s1[i] == ' ':
            i += 1
        for j in range(len(s2)):
            while s2[j] == ' ':
                j += 1
            if s2[j] == s1[i]:
                return s2[j]


print(first_match(" test", "  pters "))


def find_max_occurred_word(birds):
    """
    If more than one word with same number of maximum occurrence,
    first appeared word in list should return
    """
    a = []
    max_count = 0
    max_bird = ""
    for i in birds:
        if i not in a:
            a.append(i)

    for i in range(len(a)):
        count = birds.count(a[i])
        if count > max_count:
            max_bird = a[i]
            max_count = count

    return max_bird


print(find_max_occurred_word(["parrot", "wood", "sparrow", "wood",
                             "sparrow", "sparrow", "wood"]))
print(find_max_occurred_word(["parrot", "wood", "sparrow", "wood",
                             "wood", "sparrow", "sparrow", "sparrow"]))
print(find_max_occurred_word([]))
