import numpy as np

# Define the vocabulary and primes
vocabulary = {"0": 3, "1": 5, "2": 7, "3": 11, "4": 13, "+": 2}

# Initialize embeddings (simplified 2D vectors for illustration)
embeddings = {
    "0": np.array([0.2, 0.3]),
    "1": np.array([0.4, 0.5]),
    "2": np.array([0.6, 0.7]),
    "3": np.array([0.8, 0.9]),
    "4": np.array([1.0, 1.1]),
    "+": np.array([1.2, 1.3]),
}

# Define a function to create a "partial_add" embedding
def partial_add_embed(operand):
    return operand + embeddings["+"]
    
# Example sentence: "2+3"
operands = ["2", "3"]
partial_add_embed_2 = partial_add_embed(embeddings[operands[0]])

# Apply left-to-right outer-to-inner order
result = partial_add_embed_2 + embeddings[operands[1]]

print(f"Sentence: {operands[0]}+{operands[1]}")
print(f"Partial Addition Embedding: {partial_add_embed_2}")
print(f"Resulting Embedding: {result}")
