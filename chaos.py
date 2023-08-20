from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt

# Lattice parameters
n = 128  # Dimension
q = 2**13 - 1  # Modulus

# Random number generator
rng = np.random.default_rng()

# Gaussian distribution sampling function
def sample_gaussian(size):
    return rng.normal(0, 1, size) % q

# Lattice key generation function
def lattice_keygen():
    s = rng.integers(0, q, n) % q
    A = rng.integers(0, q, (n, n)) % q
    e = sample_gaussian(n)
    b = (A @ s + e) % q
    public_key = (A, b)
    private_key = s
    return public_key, private_key

# Chaos map function
def chaos_map(x: float, r: float) -> float:
    return r * x * (1 - x)

# Encapsulation function
def lattice_chaos_encapsulation(message: str, public_key: tuple, r: float = 3.9) -> tuple:
    A, b = public_key
    random_vector = np.random.randint(0, 2, A.shape[1])
    error_vector = np.random.normal(0, 1, A.shape[0])
    u = np.dot(A, random_vector) + error_vector
    initial_condition = 0.5
    encrypted_message = ""
    for char in message:
        initial_condition = chaos_map(initial_condition, r)
        key = ord(char) + int(initial_condition * 256)
        encrypted_message += chr(key % 256)
    return encrypted_message, u

# Decapsulation function
def lattice_chaos_decapsulation(encrypted_message: str, u: np.ndarray, private_key: np.ndarray, r: float = 3.9) -> str:
    A, s = private_key
    v = u - np.dot(A, s)
    initial_condition = 0.5
    decrypted_message = ""
    for char in encrypted_message:
        initial_condition = chaos_map(initial_condition, r)
        key = ord(char) - int(initial_condition * 256)
        decrypted_message += chr(key % 256)
    return decrypted_message

# Parameters for benchmarking
num_executions_lattice = 100
message_length_lattice = 100

# Benchmarking function
def benchmark_chaos_lattice():
    keygen_times = []
    encapsulation_times = []
    decapsulation_times = []
    for _ in range(num_executions_lattice):
        # Key generation
        start_time = timer()
        public_key, private_key = lattice_keygen()
        end_time = timer()
        keygen_times.append(end_time - start_time)
        # Encapsulation
        message = "A" * message_length_lattice
        start_time = timer()
        encrypted_message, u = lattice_chaos_encapsulation(message, public_key)
        end_time = timer()
        encapsulation_times.append(end_time - start_time)
        # Decapsulation
        start_time = timer()
        decrypted_message = lattice_chaos_decapsulation(encrypted_message, u, (public_key[0], private_key))
        end_time = timer()
        decapsulation_times.append(end_time - start_time)
    # Converting time to cycles
    keygen_cycles = sum(keygen_times) * 2.9e9 / num_executions_lattice
    encapsulation_cycles = sum(encapsulation_times) * 2.9e9 / num_executions_lattice
    decapsulation_cycles = sum(decapsulation_times) * 2.9e9 / num_executions_lattice
    return keygen_cycles, encapsulation_cycles, decapsulation_cycles

# Running the benchmark tests
our_keygen_cycles_lattice, our_encapsulation_cycles_lattice, our_decapsulation_cycles_lattice = benchmark_chaos_lattice()

# Kyber data
kyber_data = {
    "bikel1_m4f": [24_974_536, 3_394_030, 51_214_664],
    "bikel1_opt": [68_198_074, 5_085_537, 121_429_912],
    "hqc-rmrs-128_clean": [2_883_811, 5_236_720, 7_594_631],
    "kyber1024_clean": [1_649_604, 2_016_366, 2_159_906],
    "kyber512_clean": [636_181, 843_945, 940_320],
    "kyber768_clean": [1_059_876, 1_352_934, 1_471_055]
}

# Adding our hybrid method to Kyber data
kyber_data["chaos_lattice"] = [int(our_keygen_cycles_lattice), int(our_encapsulation_cycles_lattice), int(our_decapsulation_cycles_lattice)]

# Plotting the comparison
labels = list(kyber_data.keys())
key_gen = [data[0] for data in kyber_data.values()]
encapsulation = [data[1] for data in kyber_data.values()]
decapsulation = [data[2] for data in kyber_data.values()]
colors = ['blue' if label != "chaos_lattice" else 'red' for label in labels]
plt.figure(figsize=(12, 8))
plt.bar(labels, key_gen, color=colors, label="Key Generation")
plt.bar(labels, encapsulation, bottom=key_gen, color=colors, alpha=0.6, label="Encapsulation")
plt.bar(labels, decapsulation, bottom=[i + j for i, j in zip(key_gen, encapsulation)], color=colors, alpha=0.3, label="Decapsulation")

plt.yscale("log")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Cycles (log scale)")
plt.title("Comparison of Kyber and My Hybrid Chaos Theory Cipher")
plt.legend()
plt.tight_layout()
plt.show()