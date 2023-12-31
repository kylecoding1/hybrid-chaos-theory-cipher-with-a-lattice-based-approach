# Chaos-Lattice Cryptography System

**Table of Contents**
- [Overview](#overview)
- [Installation](#Installation)
- [Key Components](#key-components)
- [Core Functions](#core-functions)
- [Mathematical Details](#mathematical-details)
- [Testing](#Testing)
- [Performance Metrics](#Performance-Metrics)
- [Visualizations](#visualizations)
- [Conclusion](#conclusion)
- [License](#License)

## Overview
The Chaos-Lattice Cryptography System is an innovative and complex cryptographic application that combines the principles of chaotic dynamics, lattice-based cryptography, and cryptographic hash functions. It introduces a quantum-resistant method for secure communication, utilizing various mathematical concepts to ensure high levels of security, complexity, and unpredictability.

## Installation

Clone the Repository:
git clone git@github.com:kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach.git

Make sure the following libraries are installed in your Python environment:

pip install numpy scipy matplotlib



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
- The application introduces an encryption and decryption scheme that combines logistic maps, lattice-based cryptography, and hash functions. It includes:
  - Chaos-based encryption: Encrypts the message using chaotic dynamics.
  - Logistic-Lattice encapsulation: Combines chaotic dynamics with lattice-based encryption.

**Signature and Verification**
- Hash-based signing and verification are implemented using SHA-3 and HMAC.

## Mathematical Details
**Combined Chaos Map**
- The combined chaos map evolves three variables (x, y, z):
  - x_next = r * x * (1 - x)
  - y_next = 1 - a * y^2 + b * x
  - z_next = z * (1 - y)
  These equations are iteratively applied to create chaotic dynamics, leading to high sensitivity to initial conditions and complex behavior.

**Ring-LWE**
- The Ring-LWE problem is defined over polynomial rings and is based on the hardness of finding solutions to noisy linear equations. It's a promising candidate for post-quantum cryptography, providing security under quantum attacks.

**Entropy Calculation**
- Entropy H is calculated using the formula:
  - H = -sum(p_i * log2(p_i))
  where p_i are the probabilities of unique characters in the message. It quantifies the randomness and unpredictability of the information.

**Polynomial Arithmetic**
- FFT-based polynomial arithmetic is used for efficient polynomial operations such as addition, subtraction, multiplication, and reduction. The FFT helps in reducing the computational complexity for polynomial multiplication.

**Dynamic Key Evolution**
- The shared secret key is evolved using the combined chaos map, with an iterative process that utilizes chaotic dynamics. This introduces additional complexity and unpredictability into the key management process.


## Testing
**Entropy Calculation**
- Entropy is used to quantify the randomness and uncertainty within the encrypted message. It's calculated using Shannon's entropy formula.
- Original Message Entropy: 1.2987949406953985
- Encrypted Message Entropy: 7.091466437621499
- Decrypted Message Entropy: 1.2987949406953985

**Brute-force Analysis**
- Key space size: 340282366920938463463374607431768211456
- Time to perform exhaustive search (years): 1.0790283070806015e+22


**Randomness Testing**
- The sequence passed the monobit test, showing that the encrypted message has a balanced number of 0s and 1s.

## Performance Metrics
**Cycle Counts**
- Key Generation Time (seconds): 0.00010380000458098948
- Encryption Time (seconds): 0.00035390001721680164
- Decryption Time (seconds): 0.00021920001017861068
- Key Generation Cycles: 311400.01374296844
- Encryption Cycles: 1061700.051650405
- Decryption Cycles: 657600.030535832

## Visualizations
### Comparison of Execution Times
![Screenshot 2023-08-23 113443](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/28042582-425f-456d-920e-355454d38dca)
   This chart illustrates the execution times of various cryptographic operations, including key generation, encryption, and decryption. The x-axis represents the operation type, and the y-axis represents the time taken in seconds or CPU cycles.

### Comparison of Key Evolution: Chaos-Lattice vs Kyber & AES
![Comparison-of-Key-Evolution--Chaos-Lattice-vs-Kyber- -AES](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/d591c487-7f39-4b2f-9d03-36e4b2e812de)
The key evolution graph illustrates the dynamic nature of the Chaos-Lattice system compared to the static nature of Kyber and AES. Dynamic key evolution can enhance security by making it more difficult for an attacker to predict or find a pattern in the key sequence. This visual representation allows you to understand how keys change over iterations and can give insights into the robustness of the Chaos-Lattice system against certain types of attacks.

## Conclusion
The Chaos-Lattice Cryptography System is a complex cryptographic scheme that offers advantages in terms of complexity, unpredictability, and quantum resistance. By leveraging chaotic dynamics, lattice-based cryptography, and cryptographic hash functions, it introduces a robust and multifaceted approach to secure communication.

## License
MIT
