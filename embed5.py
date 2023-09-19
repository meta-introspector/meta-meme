# Sure, you can certainly add a unique prime number to the end of the vector for the positional information. This can help make the positional vectors more distinct and separate them from the embeddings of the tokens.

# Here's how you can modify the script to include a unique prime value for the positional information:

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
encoding_matrix = np.zeros((num_tokens, num_positions, 6))  # Add one more dimension for the unique prime
for token_index, token in enumerate(vocabulary):
    for position_index in range(num_positions):
        # Multiply embeddings by (position_index + 1) and add a unique prime value
        embedding_with_position = embeddings[token] * (position_index + 1)
        embedding_with_position[-1] = position_index + 2  # Use a unique prime for the last dimension
        encoding_matrix[token_index, position_index, :] = embedding_with_position

# Print the encoding matrix
for matrix in encoding_matrix:
    print(matrix)
# ```

# In this script, I've modified the `encoding_matrix` to have one more dimension to accommodate the unique prime value for the positional information. The last value in each vector is set to `position_index + 2` to ensure uniqueness for the position.

# Feel free to adjust the prime value used for the last dimension according to your preference. This should result in positional vectors that are distinct from the token embeddings and from each other.
