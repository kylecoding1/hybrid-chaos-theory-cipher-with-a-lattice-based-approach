from hashlib import sha256
import hmac
import numpy as np
from numpy.random import Generator, PCG64
import secrets

# HMAC function
def hmac_sha256(key, message):
    return hmac.new(key, message, sha256).digest()

# Seeding the cryptographically secure random generator
secure_seed = secrets.randbits(128)
rng = Generator(PCG64(secure_seed))

# Lattice parameters
n = 128
q = 2**13 - 1

# Gaussian distribution sampling function
def sample_gaussian(size):
    return rng.normal(0, 1, size) % q

# Lattice key generation function
def lattice_keygen():
    s = rng.integers(0, q, n) % q
    A = rng.integers(0, q, (n, n)) % q
    e = rng.normal(0, 1, n) % q
    b = (A @ s + e) % q
    public_key = (A, b)
    private_key = s
    return public_key, private_key

# Chaos map function
def chaos_map(x: float, r: float) -> float:
    return r * x * (1 - x)

# Modified encapsulation function to include lattice-based operations
def lattice_chaos_encapsulation_with_lattice(message: str, public_key: tuple, shared_secret_key, r: float = 3.9) -> tuple:
    A, b = public_key
    seed = secrets.randbits(128)
    rng = Generator(PCG64(seed))
    random_vector = rng.integers(0, q, A.shape[1]) % q
    error_vector = sample_gaussian(A.shape[0])
    u = (A @ random_vector + error_vector) % q
    initial_condition = 0.5
    encrypted_message = ""
    for char in message:
        initial_condition = chaos_map(initial_condition, r)
        key = ord(char) + int(initial_condition * 256)
        encrypted_message += chr(key % 256)
    
    # Compute MAC
    mac = hmac_sha256(shared_secret_key, encrypted_message.encode('utf-8'))

    return encrypted_message, u, mac

# Modified decapsulation function to include lattice-based operations
def lattice_chaos_decapsulation_with_lattice(encrypted_message: str, u: np.ndarray, private_key: np.ndarray, shared_secret_key, received_mac, r: float = 3.9) -> str:
    A, s = private_key
    v = (u - (A @ s)) % q
    initial_condition = 0.5
    decrypted_message = ""
    for char in encrypted_message:
        initial_condition = chaos_map(initial_condition, r)
        key = ord(char) - int(initial_condition * 256)
        decrypted_message += chr(key % 256)
    
    # Verify MAC
    computed_mac = hmac_sha256(shared_secret_key, encrypted_message.encode('utf-8'))
    if computed_mac != received_mac:
        raise Exception("MAC verification failed")

    return decrypted_message
