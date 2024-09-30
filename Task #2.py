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

# Create an empty dictionary to hold the common results
common_dict = {}

# Iterate through each dictionary in the list of random dictionaries
for i, d in enumerate(random_dicts):
    # Iterate through each key-value pair in the current dictionary
    for key, value in d.items():
        # Check if the key is already in the common dictionary
        if key in common_dict:
            # If it is, compare the current value with the existing value
            if value > common_dict[key][0]:
                # If the current value is greater, update the common dict
                common_dict[key] = (value, f"{key}_{i + 1}")  # Store value and new key name
        else:
            # If the key is not in common_dict, add it with its value and original key
            common_dict[key] = (value, f"{key}_{i + 1}")

# Prepare the final dictionary with the required format
final_dict = {}
for key, (value, new_key) in common_dict.items():
    final_dict[new_key] = value  # Use the new key name for the final dictionary

print(final_dict)