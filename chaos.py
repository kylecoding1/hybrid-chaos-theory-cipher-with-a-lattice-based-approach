
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
import secrets
from numpy.random import Generator, PCG64

# Lattice parameters
n = 128
q = 2**13 - 1

# Gaussian distribution sampling function
def sample_gaussian(size):
    seed = secrets.randbits(128)
    rng = Generator(PCG64(seed))
    return rng.normal(0, 1, size) % q

# Lattice key generation function
def lattice_keygen():
    seed = secrets.randbits(128)
    rng = Generator(PCG64(seed))
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

# Modified encapsulation function to include lattice-based operations
def lattice_chaos_encapsulation_with_lattice(message: str, public_key: tuple, r: float = 3.9) -> tuple:
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
    return encrypted_message, u

# Modified decapsulation function to include lattice-based operations
def lattice_chaos_decapsulation_with_lattice(encrypted_message: str, u: np.ndarray, private_key: np.ndarray, r: float = 3.9) -> str:
    A, s = private_key
    v = (u - (A @ s)) % q
    initial_condition = 0.5
    decrypted_message = ""
    for char in encrypted_message:
        initial_condition = chaos_map(initial_condition, r)
        key = ord(char) - int(initial_condition * 256)
        decrypted_message += chr(key % 256)
    return decrypted_message

# Benchmarking function for the modified chaos-lattice approach with lattice
def benchmark_chaos_lattice_with_lattice():
    keygen_times = []
    encapsulation_times = []
    decapsulation_times = []
    for _ in range(10):  # Reduced iterations to 10 for quicker execution
        start_time = timer()
        public_key, private_key = lattice_keygen()
        end_time = timer()
        keygen_times.append(end_time - start_time)
        message = "A" * 100
        start_time = timer()
        encrypted_message, u = lattice_chaos_encapsulation_with_lattice(message, public_key)
        end_time = timer()
        encapsulation_times.append(end_time - start_time)
        start_time = timer()
        decrypted_message = lattice_chaos_decapsulation_with_lattice(encrypted_message, u, (public_key[0], private_key))
        end_time = timer()
        decapsulation_times.append(end_time - start_time)
    keygen_cycles = sum(keygen_times) * 2.9e9 / 10
    encapsulation_cycles = sum(encapsulation_times) * 2.9e9 / 10
    decapsulation_cycles = sum(decapsulation_times) * 2.9e9 / 10
    return keygen_cycles, encapsulation_cycles, decapsulation_cycles

# Running the benchmark tests for the modified version with lattice
our_keygen_cycles_lattice_with_lattice, our_encapsulation_cycles_lattice_with_lattice, our_decapsulation_cycles_lattice_with_lattice = benchmark_chaos_lattice_with_lattice()

# Benchmark results for the modified version
benchmark_results_with_lattice = {
    "Chaos-Lattice with Lattice (Key Generation)": our_keygen_cycles_lattice_with_lattice,
    "Chaos-Lattice with Lattice (Encapsulation)": our_encapsulation_cycles_lattice_with_lattice,
    "Chaos-Lattice with Lattice (Decapsulation)": our_decapsulation_cycles_lattice_with_lattice
}

# Kyber data
kyber_data = {
    "bikel1_m4f": [24_974_536, 3_394_030, 51_214_664],
    "bikel1_opt": [68_198_074, 5_085_537, 121_429_912],
    "hqc-rmrs-128_clean": [2_883_811, 5_236_720, 7_594_631],
    "kyber1024_clean": [1_649_604, 2_016_366, 2_159_906],
    "kyber512_clean": [636_181, 843_945, 940_320],
    "kyber768_clean": [1_059_876, 1_352_934, 1_471_055]
}

# Adding Chaos-Lattice data
kyber_data["Chaos-Lattice"] = [int(our_keygen_cycles_lattice_with_lattice), int(our_encapsulation_cycles_lattice_with_lattice), int(our_decapsulation_cycles_lattice_with_lattice)]

# Function to plot comparison between Chaos-Lattice and all Kyber models
def plot_all_kyber_comparisons(title, stage_index, stage_name):
    labels = list(kyber_data.keys())
    values = [data[stage_index] for data in kyber_data.values()]
    colors = ['blue' if label != "Chaos-Lattice" else 'red' for label in labels]

    plt.figure(figsize=(12, 8))
    plt.bar(labels, values, color=colors)
    plt.yscale("log")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Cycles (log scale)")
    plt.title(f"{title}: Chaos-Lattice vs Kyber Models")
    plt.tight_layout()
    plt.show()

# Plotting comparisons for all stages
plot_all_kyber_comparisons("Key Generation Comparison", 0, "Key Generation")
plot_all_kyber_comparisons("Encapsulation Comparison", 1, "Encapsulation")
plot_all_kyber_comparisons("Decapsulation Comparison", 2, "Decapsulation")