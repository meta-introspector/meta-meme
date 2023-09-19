import numpy as np
import matplotlib.pyplot as plt

# Define the vocabulary and primes
vocabulary = {"1": 3, "2": 5, "3": 7, "+": 2}

# Initialize embeddings (using prime values or multiples of prime values)
embeddings = {
    "1": np.array([3, 3, 3, 3, 3]),  # Using prime value 3
    "2": np.array([5, 5, 5, 5, 5]),  # Using prime value 5
    "3": np.array([7, 7, 7, 7, 7]),  # Using prime value 7
    "+": np.array([2, 2, 2, 2, 2]),  # Using prime value 2
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
