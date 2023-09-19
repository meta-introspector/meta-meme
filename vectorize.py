import numpy as np
from scipy.fft import fft
import numpy as np
from scipy.fft import fft, ifft

# Replace this with your actual sequence of prime numbers
prime_sequence = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# Perform FFT on the prime sequence
fft_result = fft(prime_sequence)

# Plot the magnitude of the FFT result
import matplotlib.pyplot as plt

plt.figure()
plt.plot(np.abs(fft_result))
plt.title('FFT Magnitude')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.show()

# Replace this with your actual FFT result (frequency samples)
fft_result = np.array([10 + 0j, -5 + 5j, 0 + 0j, -5 - 5j])

# Perform the Inverse FFT to obtain the original sequence
original_sequence = ifft(fft_result)

print("Original Sequence:")
print(original_sequence)
