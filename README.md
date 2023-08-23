# Chaos-Lattice Cryptography System

**Table of Contents**
- [Overview](#overview)
- [Key Components](#key-components)
- [Core Functions](#core-functions)
- [Testing](Testing)
- [Mathematical Details](#mathematical-details)
- [Performance Metrics](#Performance-Metrics)
- [Visualizations](#visualizations)
- [Conclusion](#conclusion)
- [License](#License)

## Overview
The Chaos-Lattice Cryptography System is an innovative and complex cryptographic application that combines the principles of chaotic dynamics, lattice-based cryptography, and cryptographic hash functions. It introduces a quantum-resistant method for secure communication, utilizing various mathematical concepts to ensure high levels of security, complexity, and unpredictability.

## Key Components
1. **Chaotic Maps**
   - Chaos theory is applied using a combined chaos map, which iteratively evolves three variables (x, y, z) according to specific equations. These chaotic dynamics introduce high complexity and sensitivity to initial conditions.

2. **Ring-LWE (Ring Learning with Errors)**
   - Ring-LWE is a lattice-based cryptographic problem that forms the basis of the key generation process. It provides security based on the hardness of finding short vectors in a lattice.

3. **Dynamic Key Management**
   - An evolving key mechanism is implemented to enhance unpredictability. The key is evolved using the combined chaos map, making it highly sensitive to the initial shared secret.

4. **Hash Functions and HMAC**
   - SHA-3 (Secure Hash Algorithm 3) and HMAC (Hash-based Message Authentication Code) are employed for authentication and integrity verification.

5. **FFT-based Polynomial Arithmetic**
   - Fast Fourier Transform (FFT) is used for efficient polynomial multiplication in the Ring-LWE operations.

## Core Functions
**Key Generation**
- Two different key generation methods are implemented:
  - Lattice Key Generation: Utilizes Ring-LWE to generate a public-private key pair.
  - Hash Key Generation: Generates a 256-bit secret key.

**Encryption and Decryption**
- The application introduces a novel encryption and decryption scheme that combines logistic maps, lattice-based cryptography, and hash functions. It includes:
  - Chaos-based encryption: Encrypts the message using chaotic dynamics.
  - Logistic-Lattice encapsulation: Combines chaotic dynamics with lattice-based encryption.

**Signature and Verification**
- Hash-based signing and verification are implemented using SHA-3 and HMAC.

## Testing
**Entropy Calculation**
- Entropy is used to quantify the randomness and uncertainty within the encrypted message. It's calculated using Shannon's entropy formula.

**Performance Metrics**
- Execution times for key generation, encryption, and decryption are measured in both seconds and CPU cycles.

**Visualization and Comparison**
- The application includes a series of plots to visualize and compare the Chaos-Lattice system with other cryptographic algorithms like AES and Kyber.

## Mathematical Details
**Combined Chaos Map**
- The combined chaos map evolves three variables (x, y, z):
  - x_next = r * x * (1 - x)
  - y_next = 1 - a * y^2 + b * x
  - z_next = z * (1 - y)

**Ring-LWE**
- The Ring-LWE problem is defined over polynomial rings and is based on the hardness of finding solutions to noisy linear equations. It's a promising candidate for post-quantum cryptography.

**Entropy Calculation**
- Entropy H is calculated using the formula:
  - H = -∑(p_i * log2(p_i))
  where p_i are the probabilities of unique characters in the message.

# Performance Metrics

**Cycle Counts**
- key_generation_cycles = 305400.0117117539
- encryption_cycles = 1220999.998622574
- decryption_cycles = 881399.9884296209

**Entropy Encapsulation**
- 7.120012603669693


## Visualizations

### Comparison of Execution Times.
![Screenshot 2023-08-23 120100](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/0eeb8854-ee33-4e59-9734-97fa8e4de791)
   This chart illustrates the execution times of various cryptographic operations, including key generation, encryption, and decryption. The x-axis represents the operation type, and the y-axis represents the time taken in seconds or CPU cycles. The comparison provides insights into the performance of Chaos-Lattice/Kyber systems.

### Comparison of Key Evolution: Chaos-Lattice vs Kyber & AES
![Comparison-of-Key-Evolution--Chaos-Lattice-vs-Kyber- -AES](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/d591c487-7f39-4b2f-9d03-36e4b2e812de)
The key evolution graph illustrates the dynamic nature of the Chaos-Lattice system compared to the static nature of Kyber and AES. Dynamic key evolution can enhance security by making it more difficult for an attacker to predict or find a pattern in the key sequence. This visual representation allows you to understand how keys change over iterations and can give insights into the robustness of the Chaos-Lattice system against certain types of attacks.

## Conclusion
The Chaos-Lattice Cryptography System is a novel and complex cryptographic scheme that offers potential advantages in terms of complexity, unpredictability, and quantum resistance. By leveraging chaotic dynamics, lattice-based cryptography, and cryptographic hash functions, it introduces a robust and multifaceted approach to secure communication.

## License
MIT
