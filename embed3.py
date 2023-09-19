# I apologize for the confusion. It seems that I misunderstood your request. If you're seeing the same value (3) repeated in each dimension of the embedding vectors, then there might be an error in the way I adjusted the embeddings. 

# Let's ensure we're using distinct prime values or multiples of prime values for each dimension of the embedding vectors:

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
        encoding_matrix[token_index, position_index, :] = embeddings[token]

# Print the encoding matrix
for matrix in encoding_matrix:
    print(matrix)
# ```

# This script ensures that each dimension of the embedding vectors uses a distinct prime value or a multiple of a prime value.

# Again, I apologize for any confusion earlier. Please give this script a try to ensure that the embedding values align with your intention to use prime values or multiples of prime values.
