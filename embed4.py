# I apologize for the continued confusion. It seems that I provided you with an incorrect script again. Thank you for your patience. Here's the corrected version of the script that generates distinct embeddings for each token and position:

# ```python
import numpy as np
import matplotlib.pyplot as plt

# Define the vocabulary and primes
vocabulary = {"1": 3, "2": 5, "3": 7, "+": 2}

# Initialize embeddings (using prime values or multiples of prime values)
embeddings = {
    "1": np.array([3, 5, 7, 11, 13]),  # Using prime values
    "2": np.array([5, 7, 11, 13, 17]),  # Using prime values
    "3": np.array([7, 11, 13, 17, 19]),  # Using prime values
    "+": np.array([2, 3, 5, 7, 11]),  # Using prime values
}

# Initialize the matrix of vectors for encoding
num_tokens = len(vocabulary)
num_positions = 10

# Create the matrix by stacking embeddings for each token and position
encoding_matrix = np.zeros((num_tokens, num_positions, 5))
for token_index, token in enumerate(vocabulary):
    for position_index in range(num_positions):
        encoding_matrix[token_index, position_index, :] = embeddings[token] * (position_index + 1)

# Print the encoding matrix
for matrix in encoding_matrix:
    print(matrix)
# ```

# In this corrected version of the script, I've multiplied the embeddings by `(position_index + 1)` to ensure that each position has a distinct vector. This should provide you with distinct embeddings for each token and position.

# I apologize for any confusion caused by my previous responses. Please give this script a try, and it should give you the expected distinct embeddings.