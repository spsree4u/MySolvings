"""
Write a braces/brackets/parentheses validator.

O(n) time (one iteration through the string), and O(n) space (in the worst
case, all of our characters are openers, so we push them all onto the stack).

"""


def is_valid(code_text):
    opener_closer_map = {'{': '}', '[': ']', '(': ')'}
    openers = set(opener_closer_map.keys())
    closers = set(opener_closer_map.values())

    openers_stack = []
    for char in code_text:
        if char in openers:
            openers_stack.append(char)

        elif char in closers:
            if not openers_stack:
                return False
            else:
                last_inserted_opener = openers_stack.pop()
                if not opener_closer_map[last_inserted_opener] == char:
                    return False

    return openers_stack == []


print(is_valid("[()]{[]()}"))
print(is_valid("[{]}"))
print(is_valid("[])"))
print(is_valid("[]("))
print(is_valid("{(([])[])[]]}"))


"""
Write a function that, given a sentence like the one above, 
along with the position of an opening parenthesis, 
finds the corresponding closing parenthesis
O(n) time
O(1) space as range (generator  function) is used instead of whole list
"""


def get_closing_index(s, opening_index):
    open_paren_count = 0
    for i in range(opening_index+1, len(s)):
        if s[i] == "(":
            open_paren_count += 1
        elif s[i] == ")":
            if open_paren_count == 0:
                return i
            else:
                open_paren_count -= 1
    return "No closing parenthesis"


print(get_closing_index("Sometimes (when I nest them (my parentheticals) "
                        "too much (like this (and this))) "
                        "they get confusing.", 10))


def check_parentheses(s):
    if not s:
        print("Invalid expression!")
        return False
    stack = []
    par_map = {']': '[', ')': '(', '}': '{'}
    for char in s:
        if char in ['{', '[', '(']:
            stack.append(char)
        elif char in ['}', ']', ')']:
            last_char = stack.pop()
            if last_char != par_map[char]:
                return False
    return True


# print(check_parentheses("[()]{}{[()()]()}"))
# print(check_parentheses("[(])"))
