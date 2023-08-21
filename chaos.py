from hashlib import sha3_256
import hmac
import numpy as np
from numpy.random import Generator, PCG64
import secrets
from typing import Tuple

# Quantum-resistant hash function (SHA-3)
def hmac_sha3(key, message):
    return hmac.new(key, message, sha3_256).digest()

def combined_chaos_map(x: float, y: float, r: float = 3.9, a: float = 1.4, b: float = 0.3) -> Tuple[float, float]:
    x_next = r * x * (1 - x)
    y_next = 1 - a * y**2 + b * x
    return x_next % 1, y_next % 1

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

def logistic_lattice_chaos_encapsulation(message: str, public_key: tuple, shared_secret_key) -> Tuple[str, np.ndarray, bytes, float]:
    A, b = public_key
    seed = secrets.randbits(128)
    rng = Generator(PCG64(seed))
    random_vector = rng.integers(0, q, A.shape[1]) % q
    error_vector = sample_gaussian(A.shape[0])
    u = (A @ random_vector + error_vector) % q
    iv = rng.random()
    x_initial, y_initial = iv, 0.5
    encrypted_message = ""
    for char in message:
        x_initial, y_initial = combined_chaos_map(x_initial, y_initial)
        key = ord(char) + int((x_initial + y_initial) * 256)
        encrypted_message += chr(int(key) % 256)
    mac = hmac_sha3(shared_secret_key, encrypted_message.encode('utf-8'))
    return encrypted_message, u, mac, iv

def logistic_lattice_chaos_decapsulation(encrypted_message: str, u: np.ndarray, private_key, shared_secret_key, received_mac, iv: float) -> str:
    A, b = public_key
    v = (u - (A @ private_key)) % q
    x_initial, y_initial = iv, 0.5
    decrypted_message = ""
    for char in encrypted_message:
        x_initial, y_initial = combined_chaos_map(x_initial, y_initial)
        key = ord(char) - int((x_initial + y_initial) * 256)
        decrypted_message += chr(int(key) % 256)
    computed_mac = hmac_sha3(shared_secret_key, encrypted_message.encode('utf-8'))
    if computed_mac != received_mac:
        raise Exception("MAC verification failed")
    return decrypted_message

def calculate_differential(string1: str, string2: str) -> float:
    differences = sum(c1 != c2 for c1, c2 in zip(string1, string2))
    return (differences / len(string1)) * 100

# Testing the code
message1 = "This is a test message."
message2 = "This is b test message!"
public_key, private_key = lattice_keygen()
shared_secret_key = secrets.token_bytes(16)
encrypted_message1, u1, mac1, iv1 = logistic_lattice_chaos_encapsulation(message1, public_key, shared_secret_key)
encrypted_message2, _, _, _ = logistic_lattice_chaos_encapsulation(message2, public_key, shared_secret_key)
decrypted_message1 = logistic_lattice_chaos_decapsulation(encrypted_message1, u1, private_key, shared_secret_key, mac1, iv1)
differential_percentage = calculate_differential(encrypted_message1, encrypted_message2)

# Results
decryption_success = decrypted_message1 == message1
decryption_success, differential_percentage
