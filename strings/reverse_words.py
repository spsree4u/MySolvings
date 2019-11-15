"""
Write a function reverse_words() that takes a message as a list of characters 
and reverses the order of the words in place.

For example:

  message = [ 'c', 'a', 'k', 'e', ' ',
            'p', 'o', 'u', 'n', 'd', ' ',
            's', 't', 'e', 'a', 'l' ]

reverse_words(message)

# Prints: 'steal pound cake'
print(''.join(message))

Assume the message contains only letters and spaces,
and all words are separated by one space.

Complexity
O(n) time and O(1) space

"""


def reverse_characters(text_to_reverse, left, right):

    while left < right:
        text_to_reverse[left], text_to_reverse[right] = \
            text_to_reverse[right], text_to_reverse[left]
        left += 1
        right -= 1


def reverse_words(text_to_reverse):
    # reverse full string
    reverse_characters(text_to_reverse, 0, len(text_to_reverse)-1)

    current_word_start = 0

    for i in range(len(text_to_reverse)+1):
        # reverse back word-wise to original words
        if (i == len(text_to_reverse)) or (text_to_reverse[i] == ' '):
            reverse_characters(text_to_reverse, current_word_start, i-1)
            current_word_start = i + 1


input_text_list = ['t', 'h', 'e', ' ', 'e', 'a', 'g', 'l', 'e', ' ',
                   'h', 'a', 's', ' ', 'l', 'a', 'n', 'd', 'e', 'd']
print(input_text_list)
reverse_words(input_text_list)
print(input_text_list)


def reverse_string(s):
    new = ""
    i = len(s) - 1
    while i >= 0:
        new = new + s[i]
        i -= 1
    return new


s1 = "abcd efgh"
s2 = reverse_string(s1)
print(s2)


def reverse_words_dsa(s):
    last = start = len(s) - 1
    s2 = ''
    while last >= 0:
        while start >= 0 and s[start] == ' ':
            start -= 1

        last = start
        while start >= 0 and s[start] != ' ':
            start -= 1
        for i in range(start+1, last+1):
            s2 = s2 + s[i]

        if start > 0:
            s2 = s2 + ' '

        last = start - 1
        start = last
    return s2


print(reverse_words_dsa(" once upon a time "))
