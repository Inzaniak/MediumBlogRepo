input_string = "Hello World! This is an example of a string."

# 1. Strings are lists ###########################
example_string = input_string
print("Input String:", example_string)
print("First 5 characters:", example_string[0:5])
# This does not work!
example_string.append("!")

# 2. Reverse a string ###########################
example_string = input_string
print("Input String:", example_string)
print("Reverse String:", example_string[::-1])

# 3. In operator ###########################
example_string = input_string
print("Input String:", example_string)
print("'Hello' in input string:", "Hello" in example_string)
# In operator is case sensitive!
print("'hello' in input string:", "hello" in example_string)

# 4. Replace ###########################
example_string = input_string
print("Input String:", example_string)
print("Replace 'World' with 'Planet':", example_string.replace("World", "Planet"))

# 5. String module ###########################
import string

print("Punctuation:", string.punctuation)
print("Digits:", string.digits)
print("Lowercase:", string.ascii_lowercase)

example_string = input_string
print("Input String:", example_string)
print("Punctuation in string:", [punc for punc in example_string if punc in string.punctuation])

# 6. Text stripping ###########################
string_with_spaces = "   Hello World!   "
print("Input String:", string_with_spaces)
print("Strip spaces:", string_with_spaces.strip())

# 7. Find if a string contains numbers ###########################
example_string = input_string
print("Input String:", example_string)
print("Contains numbers:", example_string.isalpha())

