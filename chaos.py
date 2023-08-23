from hashlib import sha3_256
import hmac
import numpy as np
from numpy.random import Generator, PCG64
import secrets
from typing import Tuple
import math
from string import ascii_letters, digits
import random
import time

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

def sample_gaussian(size):
    return rng.normal(0, 1, size) % q

def lattice_keygen():
    s = rng.integers(0, q, n) % q
    A = rng.integers(0, q, (n, n)) % q
    e = rng.normal(0, 1, n) % q
    b = (A @ s + e) % q
    public_key = (A, b)
    private_key = s
    return public_key, private_key

def generate_random_padding(length=1000):
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
    random_vector = rng.integers(0, q, A.shape[1]) % q
    error_vector = sample_gaussian(A.shape[0])
    u = (A @ random_vector + error_vector) % q
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

def logistic_lattice_chaos_decapsulation(encrypted_message, u, private_key, shared_secret_key, received_mac, iv, signature, hash_secret_key):
    if not hash_verify(encrypted_message, signature, hash_secret_key):
        raise Exception("Hash signature verification failed")
    A, b = public_key  # public_key should be passed as an argument
    v = (u - (A @ private_key)) % q
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
    return decrypted_message_with_padding[1000:]

def calculate_differential(string1: str, string2: str) -> float:
    differences = sum(c1 != c2 for c1, c2 in zip(string1, string2))
    return (differences / len(string1)) * 100


def calculate_entropy(message):
    from collections import Counter
    import math
    
    frequencies = Counter(message)
    total_chars = len(message)
    
    entropy = -sum((count / total_chars) * math.log2(count / total_chars) for count in frequencies.values())
    return entropy

# Compute private key entropy
def private_key_entropy(private_key):
    return n * math.log2(q)

def key_entropy(key: bytes) -> float:
    return len(key) * math.log2(256)  # 2^8 possible values for each byte

# Test the code
message = "Test message"
public_key, private_key = lattice_keygen()
shared_secret_key = secrets.token_bytes(32)
hash_secret_key = hash_keygen()
encrypted_message, u, mac, iv, signature = logistic_lattice_chaos_encapsulation(message, public_key, shared_secret_key, hash_secret_key)
decrypted_message = logistic_lattice_chaos_decapsulation(encrypted_message, u, private_key, shared_secret_key, mac, iv, signature, hash_secret_key)

# Verify the result
decrypted_message == message

# Key Generation Timing
start_time_keygen = time.time()
public_key, private_key = lattice_keygen()
end_time_keygen = time.time()
keygen_duration = end_time_keygen - start_time_keygen

keygen_entropy = private_key_entropy(private_key)



message1 = "fcvvv "
message2 = "vvvv"
public_key, private_key = lattice_keygen() 
shared_secret_key = secrets.token_bytes(32)

# Make sure to pass hash_secret_key as the last argument to the encapsulation function
encrypted_message1, u1, mac1, iv1, signature1 = logistic_lattice_chaos_encapsulation(message1, public_key, shared_secret_key, hash_secret_key)
encrypted_message2, _, _, _, _ = logistic_lattice_chaos_encapsulation(message2, public_key, shared_secret_key, hash_secret_key)
decrypted_message1 = logistic_lattice_chaos_decapsulation(encrypted_message1, u1, private_key, shared_secret_key, mac1, iv1, signature1, hash_secret_key)
differential_percentage = calculate_differential(encrypted_message1, encrypted_message2)

# Calculate entropy of keys and messages
entropy_shared_secret_key = key_entropy(shared_secret_key)

entropy_private_key = calculate_entropy(private_key.tobytes())  # Convert private_key to bytes

entropy_encrypted_message1 = calculate_entropy(encrypted_message1)
entropy_encrypted_message2 = calculate_entropy(encrypted_message2)

# Compare entropy values to estimated key entropy
key_length = len(shared_secret_key)
possible_values = 256  # 2^8 possible values for each byte
key_entropy = key_length * math.log2(possible_values)
# Key Generation Timing
start_time_keygen = time.time()
public_key, private_key = lattice_keygen()
end_time_keygen = time.time()
keygen_duration = end_time_keygen - start_time_keygen

# Encryption Timing
start_time_enc = time.time()
encrypted_message1, u1, mac1, iv1, signature1 = logistic_lattice_chaos_encapsulation(message1, public_key, shared_secret_key, hash_secret_key)
end_time_enc = time.time()
encryption_duration = end_time_enc - start_time_enc

# Decryption Timing
start_time_dec = time.time()
decrypted_message1 = logistic_lattice_chaos_decapsulation(encrypted_message1, u1, private_key, shared_secret_key, mac1, iv1, signature1, hash_secret_key)
end_time_dec = time.time()
decryption_duration = end_time_dec - start_time_dec


# Print Results


# Results
decryption_success = decrypted_message1 == message1
print("Decryption success:", decryption_success)
print("Differential percentage:", differential_percentage)
print("Entropy of encrypted message 1:", entropy_encrypted_message1)
print("Entropy of encrypted message 2:", entropy_encrypted_message2)
print("Estimated key entropy:", key_entropy, "bits")
print("Key Generation Time:", keygen_duration, "seconds")
print("Encryption Time:", encryption_duration, "seconds")
print("Decryption Time:", decryption_duration, "seconds")
print("Private Key Entropy:", keygen_entropy, "bits")
print("Entropy of shared secret key:", entropy_shared_secret_key, "bits")