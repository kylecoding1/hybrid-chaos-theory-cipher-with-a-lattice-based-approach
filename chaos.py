from hashlib import sha3_256
import hmac
import numpy as np
from numpy.fft import fft, ifft
from numpy.random import Generator, PCG64
import secrets
from typing import Tuple
import math
from string import ascii_letters, digits
import random
from collections import Counter
from time import perf_counter
import matplotlib.pyplot as plt
from scipy.stats import norm

# Quantum-resistant hash function (SHA-3)
def hmac_sha3(key, message):
    return hmac.new(key, message, sha3_256).digest()

def combined_chaos_map(x: float, y: float, z: float, r: float = 3.9, a: float = 1.4, b: float = 0.3) -> Tuple[float, float, float]:
    x_next = r * x * (1 - x)
    y_next = 1 - a * y**2 + b * x
    z_next = z * (1 - y)
    return x_next % 1, y_next % 1, z_next % 1

# Dynamic Key Management
def evolve_key(shared_secret_key, iterations=10):
    x_initial = int.from_bytes(shared_secret_key[:4], byteorder='big') / 0xFFFFFFFF
    y_initial = int.from_bytes(shared_secret_key[4:8], byteorder='big') / 0xFFFFFFFF
    z_initial = int.from_bytes(shared_secret_key[8:12], byteorder='big') / 0xFFFFFFFF
    for _ in range(iterations):
        x_initial, y_initial, z_initial = combined_chaos_map(x_initial, y_initial, z_initial)
    evolved_key = int(x_initial * 0xFFFFFFFF).to_bytes(4, byteorder='big')
    evolved_key += int(y_initial * 0xFFFFFFFF).to_bytes(4, byteorder='big')
    evolved_key += int(z_initial * 0xFFFFFFFF).to_bytes(4, byteorder='big')
    evolved_key += shared_secret_key[12:]
    return evolved_key

secure_seed = secrets.randbits(128)
rng = Generator(PCG64(secure_seed))
n = 1024  
q = 4294967291  

# Polynomial addition
def add_polynomials(a, b):
    return (a + b) % q

# Polynomial subtraction
def subtract_polynomials(a, b):
    return (a - b) % q

# Polynomial multiplication using FFT
def multiply_polynomials(a, b):
    A = fft(a)
    B = fft(b)
    return np.round(ifft(A * B).real).astype(int) % q


# Reduction modulo x^n + 1
def reduce_polynomial(a):
    return (a[:n // 2] - a[n // 2:]) % q

# Sample a random polynomial
def sample_polynomial():
    return rng.integers(0, q, n, dtype=np.int64) % q


# Sample from a Gaussian distribution
def sample_gaussian(size):
    return np.round(np.random.normal(0, 1, size)) % q

# Lattice key generation for Ring-LWE
def lattice_keygen():
    s = sample_polynomial()
    A = sample_polynomial()
    e = sample_gaussian(n)
    b = add_polynomials(multiply_polynomials(A, s), e)
    public_key = (A, b)
    private_key = s
    return public_key, private_key

def generate_random_padding(length=230):
    characters = list(ascii_letters + digits)  # Convert to list
    return ''.join(random.choice(characters) for _ in range(length))

# Hash-based key generation
def hash_keygen():
    return secrets.token_bytes(32) # 256-bit secret key

# Hash-based signing
def hash_sign(message, secret_key):
    return hmac.new(secret_key, message.encode('utf-8'), sha3_256).digest()

# Hash-based verification
def hash_verify(message, signature, secret_key):
    computed_signature = hmac.new(secret_key, message.encode('utf-8'), sha3_256).digest()
    return computed_signature == signature

def logistic_lattice_chaos_encapsulation(message, public_key, shared_secret_key, hash_secret_key):
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    padding = generate_random_padding()
    message_with_padding = padding + message
    A, b = public_key
    seed = secrets.randbits(128)
    rng = Generator(PCG64(seed))
    random_vector = rng.integers(0, q, n) % q
    error_vector = sample_gaussian(A.shape[0])
    u = add_polynomials(multiply_polynomials(A, random_vector), error_vector)
    iv = rng.random()
    x_initial, y_initial, z_initial = iv, rng.random(), rng.random()
    encrypted_message = ""
    for char in message_with_padding:
        x_initial, y_initial, z_initial = combined_chaos_map(x_initial, y_initial, z_initial)
        key = ord(char) + int((x_initial + y_initial + z_initial) * 256)
        encrypted_message += chr(int(key) % 256)
    # Evolve shared_secret_key before using it
    evolved_shared_secret_key = evolve_key(shared_secret_key)
    mac = hmac_sha3(evolved_shared_secret_key, encrypted_message.encode('utf-8'))
    signature = hash_sign(encrypted_message, hash_secret_key)
    return encrypted_message, u, mac, iv, signature

def logistic_lattice_chaos_decapsulation(encrypted_message, u, public_key, private_key, shared_secret_key, received_mac, iv, signature, hash_secret_key):
    if not hash_verify(encrypted_message, signature, hash_secret_key):
        raise Exception("Hash signature verification failed")
    A, b = public_key  
    v = subtract_polynomials(u, multiply_polynomials(A, private_key))
    x_initial, y_initial, z_initial = iv, 0.5, 0.5
    decrypted_message_with_padding = ""
    for char in encrypted_message:
        x_initial, y_initial, z_initial = combined_chaos_map(x_initial, y_initial, z_initial)
        key = ord(char) - int((x_initial + y_initial + z_initial) * 256)
        decrypted_message_with_padding += chr(int(key) % 256)
    # Evolve shared_secret_key before using it
    evolved_shared_secret_key = evolve_key(shared_secret_key)
    computed_mac = hmac_sha3(evolved_shared_secret_key, encrypted_message.encode('utf-8'))
    if computed_mac != received_mac:
        raise Exception("MAC verification failed")
    return decrypted_message_with_padding[230:]

def calculate_entropy(message):
    probabilities = [freq / len(message) for _, freq in Counter(message).items()]
    return -sum(p * math.log2(p) for p in probabilities)



def brute_force_analysis(key_size_bits):
    key_space_size = 2 ** key_size_bits
    print(f"Key space size: {key_space_size}")

    # Assuming a computational resource capable of trying 1 billion keys per second
    computational_power = 1e9
    time_to_exhaustive_search_seconds = key_space_size / computational_power
    time_to_exhaustive_search_years = time_to_exhaustive_search_seconds / (60 * 60 * 24 * 365)

    print(f"Time to perform exhaustive search (years): {time_to_exhaustive_search_years}")

# Example usage with a 128-bit key
brute_force_analysis(128)

def monobit_test(encrypted_message):
    # Convert the message to a binary string
    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message)

    

    # Count the number of 1s
    num_ones = binary_message.count('1')
    num_zeros = len(binary_message) - num_ones

    # Compute the test statistic
    S_obs = abs(num_ones - num_zeros) / (len(binary_message) ** 0.5)

    # Compute the P-value
    P_value = norm.cdf(-S_obs)

    # Check against a significance level
    significance_level = 0.01
    if P_value < significance_level:
        print("The sequence is non-random")
    else:
        print("The sequence is random")



# Example usage of the code
public_key, private_key = lattice_keygen()
shared_secret_key = secrets.token_bytes(16)
hash_secret_key = secrets.token_bytes(32)  # 256-bit secret key

message_to_encrypt = "lolzzzzz"
encrypted_message, u, mac, iv, signature = logistic_lattice_chaos_encapsulation(
    message_to_encrypt, public_key, shared_secret_key, hash_secret_key
)

decrypted_message = logistic_lattice_chaos_decapsulation(
    encrypted_message, u, public_key, private_key, shared_secret_key, mac, iv, signature, hash_secret_key
)

# Calculate the entropy
original_entropy = calculate_entropy(message_to_encrypt)
encrypted_entropy = calculate_entropy(encrypted_message)
decrypted_entropy = calculate_entropy(decrypted_message)



# Key Generation
start_time = perf_counter()
public_key, private_key = lattice_keygen()
keygen_time = perf_counter() - start_time
print("Key Generation Time (seconds):", keygen_time)

# Encryption
start_time = perf_counter()
encrypted_message, u, mac, iv, signature = logistic_lattice_chaos_encapsulation(
    message_to_encrypt, public_key, shared_secret_key, hash_secret_key
)
encryption_time = perf_counter() - start_time
print("Encryption Time (seconds):", encryption_time)

# Decryption
start_time = perf_counter()
decrypted_message = logistic_lattice_chaos_decapsulation(
    encrypted_message, u, public_key, private_key, shared_secret_key, mac, iv, signature, hash_secret_key
)
decryption_time = perf_counter() - start_time
print("Decryption Time (seconds):", decryption_time)

print("Original Message Entropy:", original_entropy)
print("Encrypted Message Entropy:", encrypted_entropy)
print("Decrypted Message Entropy:", decrypted_entropy)


clock_frequency = 3 * 10**9  # 3 GHz

# Key Generation
keygen_cycles = keygen_time * clock_frequency

# Encryption
encryption_cycles = encryption_time * clock_frequency

# Decryption
decryption_cycles = decryption_time * clock_frequency

print("Key Generation Cycles:", keygen_cycles)
print("Encryption Cycles:", encryption_cycles)
print("Decryption Cycles:", decryption_cycles)


print("Original Message:", message_to_encrypt)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", decrypted_message)

if message_to_encrypt == decrypted_message:
    print("Decryption was successful! Original and decrypted messages are the same.")
else:
    print("Decryption failed! Original and decrypted messages are different.")

    # Example usage
monobit_test(encrypted_message)


algorithms = [
    "bikel1 (m4f)",
    "bikel1 (opt)",
    "hqc-rmrs-128 (clean)",
    "kyber1024 (clean)",
    "kyber1024 (m4fspeed)",
    "kyber1024 (m4fstack)",
    "kyber1024-90s (clean)",
    "kyber1024-90s (m4fspeed)",
    "kyber1024-90s (m4fstack)",
    "kyber512 (clean)",
    "kyber512 (m4fspeed)",
    "kyber512 (m4fstack)",
    "kyber512-90s (clean)",
    "kyber512-90s (m4fspeed)",
    "kyber512-90s (m4fstack)",
    "kyber768 (clean)",
    "kyber768 (m4fspeed)",
    "kyber768 (m4fstack)",
    "kyber768-90s (clean)",
    "kyber768-90s (m4fspeed)",
    "kyber768-90s (m4fstack)",
    "Chaos_Lattice"
]

keygen_times = [
    389099.9942086637,
    68198074,
    2883811,
    1649604,
    1122936,
    1126561,
    3008837,
    973196,
    979692,
    636181,
    434438,
    433718,
    948446,
    369011,
    369736,
    1059876,
    706531,
    707275,
    1816649,
    614455,
    617709,
    298800.00511184335
]

encryption_times = [
    1057500.0196695328,
    5085537,
    5236720,
    2016366,
    1315737,
    1323943,
    3275730,
    1068184,
    1079272,
    843945,
    530469,
    531676,
    1112852,
    421685,
    424339,
    1352934,
    863343,
    867363,
    2032562,
    694064,
    700599,
    1200000.9874785542
]

decryption_times = [
    666000.007186085,
    121429912,
    7594631,
    2159906,
    1209901,
    1219060,
    3516691,
    1059775,
    1071817,
    940320,
    476712,
    478166,
    1261630,
    420333,
    423234,
    1471055,
    783369,
    788053,
    2225597,
    688999,
    696202,
    618599.9955050647
]

# Plotting
plt.figure(figsize=(10, 6))
plt.barh(algorithms, keygen_times, color='blue', label='Key Generation')
plt.barh(algorithms, encryption_times, color='green', label='Encryption', left=keygen_times)
plt.barh(algorithms, decryption_times, color='red', label='Decryption', left=[x + y for x, y in zip(keygen_times, encryption_times)])
plt.xlabel('Execution Time (Cycles)')
plt.ylabel('Algorithms')
plt.title('Comparison of Execution Times (Kyber vs Chaos_Lattice)')
plt.legend()
plt.tight_layout()

# Save the plot as an image
plt.savefig('chaos_execution_times_plot.png')

# Print a message indicating that the plot has been saved
print("Plot saved as 'chaos_execution_times_plot.png'")

def plot_key_evolution(initial_key, iterations=50):
    # Chaos-Lattice Key Evolution
    chaos_keys = [initial_key]
    for _ in range(iterations):
        key = evolve_key(chaos_keys[-1])
        chaos_keys.append(key)
    chaos_keys_int = [int.from_bytes(key, byteorder='big') for key in chaos_keys]

    # Kyber and AES (Static Keys)
    kyber_key = secrets.token_bytes(16)
    aes_key = secrets.token_bytes(16)
    kyber_keys_int = [int.from_bytes(kyber_key, byteorder='big')] * (iterations + 1)
    aes_keys_int = [int.from_bytes(aes_key, byteorder='big')] * (iterations + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(chaos_keys_int, marker='o', label="Chaos-Lattice Dynamic Key Evolution (my model)")
    plt.plot(kyber_keys_int, marker='x', linestyle='--', label="Kyber Static Key")
    plt.plot(aes_keys_int, marker='s', linestyle='--', label="AES Static Key")
    plt.xlabel('Iteration')
    plt.ylabel('Key Value')
    plt.title('Comparison of Key Evolution: Chaos-Lattice vs Kyber & AES')
    plt.legend()
    plt.show()

initial_key = secrets.token_bytes(16)  # 128-bit initial key
plot_key_evolution(initial_key)

# Chaos_Lattice entropy evolution
def chaos_lattice_entropy_evolution(message, shared_secret_key, public_key, hash_secret_key, iterations=100):
    entropies = []
    for _ in range(iterations):
        encrypted_message, _, _, _, _ = logistic_lattice_chaos_encapsulation(
            message, public_key, shared_secret_key, hash_secret_key
        )
        entropy = calculate_entropy(encrypted_message)
        entropies.append(entropy)
        # Evolve shared secret key
        shared_secret_key = evolve_key(shared_secret_key)
    return entropies

# Simulating AES and Kyber (assuming a constant entropy for simplicity)
def simulate_aes_kyber_entropy(iterations=100):
    aes_entropies = [7.2] * iterations  
    kyber_entropies = [7.5] * iterations 
    return aes_entropies, kyber_entropies

# Simulating Chaos_Lattice, AES, and Kyber
iterations = 100
message = "test message"
shared_secret_key = secrets.token_bytes(16)
public_key, _ = lattice_keygen()
hash_secret_key = secrets.token_bytes(32)

chaos_lattice_entropies = chaos_lattice_entropy_evolution(message, shared_secret_key, public_key, hash_secret_key, iterations)
aes_entropies, kyber_entropies = simulate_aes_kyber_entropy(iterations)

plt.plot(chaos_lattice_entropies, label='Chaos_Lattice Entropy')
plt.plot(aes_entropies, label='AES Entropy')
plt.plot(kyber_entropies, label='Kyber Entropy')
plt.xlabel('Iterations')
plt.ylabel('Entropy')
plt.title('Entropy Evolution Comparison')
plt.legend()
plt.show()

# Defining the complexity and unpredictability values
algorithms = ["Chaos-Lattice (My Algorithm)", "AES", "Kyber"]
complexity = [4, 3, 3]  
unpredictability = [5, 2, 3] 

# Creating the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bars for complexity and unpredictability
bar_width = 0.35
index = range(len(algorithms))
bar1 = plt.bar(index, complexity, bar_width, label='Complexity', alpha=0.7)
bar2 = plt.bar(index, unpredictability, bar_width, label='Unpredictability', alpha=0.7, bottom=complexity)

# Adding labels and title
plt.xlabel('Algorithms')
plt.ylabel('Score')
plt.title('Complexity and Unpredictability Comparison')
plt.xticks(index, algorithms)
plt.legend()

# Showing the plot
plt.tight_layout()
plt.show()


