import random
import string

# Identify random number of dictionaries
dict_count=random.randint(2, 10)

# Randomly determine the number of keys
num_keys=random.randint(1, len(string.ascii_lowercase))

#Create list with random dicts with random keys and random values
random_dicts=[
    {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range (num_keys)}
    for _ in range (dict_count)
]

print (random_dicts)

