import math
import hashlib
import string

def get_password(student_username, l=10):
    # Possible characters include upper-case English letters, numbers between 0 and 9 (inclusive), 
    # and the underscore symbol
    options = string.digits + string.ascii_uppercase  + "_"

    h = hashlib.sha256(("ECS759P-AI"+student_username).encode("utf-8"))
    d = h.digest()
    s = ""
    # Go over all values of d. Hash will give us a 32-byte [256 bit] value,
    # which we will convert to a string by using the values as indices in the options string
    # We will use the modulo operator to ensure that the index is within the range of the options string
    for n in d:
      s += options[n%len(options)]
    return s[0:l]

# TO DO: replace *** with your EECS username and uncomment the code
student_password = get_password('EC20433')
print("Student password", student_password)

# Distance function
def distance_function(string_one, string_two):
    score = 0
    for i, j in zip(string_one, string_two):
        # Square of the absolute difference between two Unicode codes
        score += math.sqrt(abs(ord(i) - ord(j)))
    return score


# Upper bound of the distance value
MAX_VALUE = distance_function('0000000000', '__________')

# Compute normalised fitness for a list of candidate passwords 
def get_normalised_fitness(list_of_phrases, student_password):
    ordered_dict = dict()
    phrase_to_find = student_password
    for phrase in list_of_phrases:
        # Return 1 when a candidate matches the true password (string distance between them is zero)
        ordered_dict[phrase] = 1 - distance_function(phrase, phrase_to_find) / MAX_VALUE
    return ordered_dict

# Example of how to get fitness values for a list of candidates
ordered_dict = get_normalised_fitness(['2Q4HHHHOTJ', '2HHZQYUOTJ'], student_password)
print(ordered_dict)
