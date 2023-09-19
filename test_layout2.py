# Creating an ASCII art representation of the plot using emojis is a creative way to visualize your encoding vectors. However, ASCII art might not fully capture the complexity of the layout, especially if you're working with higher-dimensional embeddings. Nevertheless, here's a basic example using emojis to represent the layout:

# ```python
import numpy as np
import matplotlib.pyplot as plt

# Define the vocabulary and primes
vocabulary = {"1": 3, "2": 5, "3": 7, "+": 2}

# Initialize embeddings (5D vectors with separate dimensions)
embeddings = {
    "1": np.array([0, 0, 1, 0, 0]),
    "2": np.array([0, 0, 0, 1, 0]),
    "3": np.array([0, 1, 0, 0, 0]),
    "+": np.array([1, 0, 0, 0, -1]),
}

# Initialize the matrix of vectors for encoding
num_tokens = len(vocabulary)
num_positions = 10

# Create the matrix by stacking embeddings for each token and position
encoding_matrix = np.zeros((num_tokens, num_positions, 5))
for token_index, token in enumerate(vocabulary):
    for position_index in range(num_positions):
        encoding_matrix[token_index, position_index, :] = embeddings[token] * (position_index + 1)

# # Apply a layout algorithm for visualization
# layout = np.zeros((num_tokens * num_positions, 2))
# for i in range(num_tokens):
#     for j in range(num_positions):
#         index = i * num_positions + j
#         layout[index, :] = encoding_matrix[i, j, :2]  # Use only the first two dimensions
print(encoding_matrix)
layout = encoding_matrix.reshape(-1, 5)
print(layout)
# Define emojis for visualization
emojis = ["😀", "😁", "😂", "🤔", "👍", "👌", "🙌", "❤️", "🔥", "🌟"]

ascii_art = ""
for y in range(num_tokens):
    for x in range(num_positions):
        idx = y * num_positions + x
        token_idx = int(min(layout[idx, 0], 1) * (len(emojis) - 1))
        #print(dict(y=y,x=x,idx=idx,tidx=token_idx, lena=len(emojis)))
        emoji = emojis[token_idx]
        ascii_art += emoji
    ascii_art += "\n"



print(ascii_art)
# ```

# Keep in mind that this is a simple example and the ASCII art representation may not be highly accurate due to the limitations of emojis in representing complex data. However, it can still give you a basic visual overview of the layout.
