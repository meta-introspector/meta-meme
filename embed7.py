import numpy as np
import matplotlib.pyplot as plt

# Define the vocabulary and primes
#vocabulary = {"1": 3, "2": 5, "3": 7, "+": 2}
vocabulary = {"1": 0, "+": 1, "2": 2, "3": 3}  # Use correct indices for each token

# Initialize embeddings (using prime values or multiples of prime values)
embeddings = {
    "1": np.array([3, 5, 7, 11, 13]),  # Using prime values
    "2": np.array([5, 7, 11, 13, 17]),  # Using prime values
    "3": np.array([7, 11, 13, 17, 19]),  # Using prime values
    "+": np.array([2, 3, 5, 7, 11]),  # Using prime values
}

# Prime numbers for the positional dimension
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

# Initialize the matrix of vectors for encoding
num_tokens = len(vocabulary)
num_positions = 10

# Create the matrix by stacking embeddings for each token and position
encoding_matrix = np.zeros((num_tokens, num_positions, 6))  # Add one more dimension for the unique prime
for token_index, token in enumerate(vocabulary):
    for position_index in range(num_positions):
        # Multiply embeddings by (position_index + 1) and add a unique prime value
        embedding_with_position = np.zeros(6)  # Create an array with shape (6)
        embedding_with_position[:5] = embeddings[token] * (position_index + 1)
        embedding_with_position[-1] = prime_numbers[position_index]  # Use prime for the last dimension
        encoding_matrix[token_index, position_index, :] = embedding_with_position
#Encode the addition table using the embeddings
for i in range(1, 3):
    for j in range(1, 3):
        expression = ["1", "+", "2"]  # Use 1 and 2 as placeholders
        expression[0] = str(i)  # Replace the placeholders with actual numbers
        expression[2] = str(j)
        encoded_expression = []
        for token in expression:

            token_idx = vocabulary[token]
            #print (dict(token=token, expression=expression,
            #            vocab=vocabulary,
            #            token_idx=token_idx, x=i - 1,
            #            shape_encoding_matrix=encoding_matrix.shape))
            encoded_expression.append(encoding_matrix[token_idx, i - 1, :])  # Use i - 1 for 1-based indexing
        result_vector = np.sum(encoded_expression, axis=0)
        print(f"Expression: {i}+{j}, Encoded Vector: {result_vector}")
        
