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
n = 1024  # Increased dimension
q = 4294967291  # Large prime number close to 2^32

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

def generate_random_padding(length=100):
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
    return decrypted_message_with_padding[100:]

def calculate_entropy(message):
    probabilities = [freq / len(message) for _, freq in Counter(message).items()]
    return -sum(p * math.log2(p) for p in probabilities)

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
    897300.0221885741
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

# ... (Previous code remains the same)

# Remove "bikel1 (opt)" from the list of algorithms




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
plt.savefig('chaosSPEED_execution_times_plot.png')

# Print a message indicating that the plot has been saved
print("Plot saved as 'chaosSPEED_execution_times_plot.png'")
