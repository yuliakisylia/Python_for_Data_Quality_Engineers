import random

# Create a list of 100 random numbers from 0 to 1000
random_numbers = [random.randint(0, 1000) for _ in range(100)]

# Bubble sort
# Start the outer loop to iterate through all elements in the list
for i in range(len(random_numbers)):
    # Start the inner loop to iterate through remaining elements
    for j in range(0, len(random_numbers) - i - 1):
        # Compare the current element with the next one
        if random_numbers[j] > random_numbers[j + 1]:
            # If the current element is greater than the next, swap them
            random_numbers[j], random_numbers[j + 1] = random_numbers[j + 1], random_numbers[j]

# Sums and counters
even_sum = 0  # Sum of even numbers
odd_sum = 0   # Sum of odd numbers
even_count = 0  # Count of even numbers
odd_count = 0   # Count of odd numbers

# Iterate through all numbers
for number in random_numbers:
    # If the number is even
    if number % 2 == 0:
        even_sum += number  # Add to the sum of even numbers
        even_count += 1  # Increase the count of even numbers
    else:
        odd_sum += number  # Add to the sum of odd numbers
        odd_count += 1  # Increase the count of odd numbers

# Calculate average values
if even_count > 0:  # Check if there are any even numbers
    even_average = even_sum / even_count  # Average of even numbers
else:
    even_average = 0  # If no even numbers, average is 0

if odd_count > 0:  # Check if there are any odd numbers
    odd_average = odd_sum / odd_count  # Average of odd numbers
else:
    odd_average = 0  # If no odd numbers, average is 0

# Print the results
print("Average of even numbers:", even_average)
print("Average of odd numbers:", odd_average)