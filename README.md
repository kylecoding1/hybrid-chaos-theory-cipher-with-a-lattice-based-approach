# Hybrid Chaos-Lattice Cipher: A Lattice-Based Approach with Chaos Theory

## Introduction
In the era of quantum computing, the landscape of cryptography is rapidly evolving. The Chaos-Lattice method, developed in our lab, is at the forefront of this evolution. This method ingeniously integrates chaos theory with lattice-based cryptography to forge a cryptographic solution that is not only innovative and efficient but also resistant to the threats posed by quantum computing. 

## Methodology

The Chaos-Lattice cryptographic scheme consists of two main components: Chaos Theory and Lattice-Based Cryptography. Here's how these elements are intertwined :

### 1. **Chaos Theory**:
   Chaos theory is leveraged through a combined chaos map that incorporates three variables. The mathematical representation is as follows:

   \[
   \begin{align*}
   x_{\text{next}} & = r \cdot x \cdot (1 - x) \\
   y_{\text{next}} & = 1 - a \cdot y^2 + b \cdot x \\
   z_{\text{next}} & = z \cdot (1 - y)
   \end{align*}
   \]

   where \( r = 3.9 \), \( a = 1.4 \), and \( b = 0.3 \). The chaos map generates pseudorandom values that contribute to the encryption process.

### 2. **Lattice-Based Cryptography**:
   A lattice-based key generation method is employed, given by:

   \[
   \begin{align*}
   s & = \text{random integers} \, \mod q \\
   A & = \text{random integers} \, \mod q \\
   e & = \text{normal distribution} \, \mod q \\
   b & = (A \cdot s + e) \, \mod q
   \end{align*}
   \]

   where \( n = 1024 \) is the dimension, and \( q = 4294967291 \) is a large prime number close to \( 2^{32} \).

### 3. **Encryption and Decryption**:
   - **Encryption**:
     The encryption process combines the chaos map with the public key (A, b) and a shared secret key. The chaos map is iteratively applied to each character of the message, and a MAC is computed using HMAC-SHA3.

   - **Decryption**:
     Decryption reverses the encryption process by applying the chaos map in reverse, along with the private key and the shared secret key.



## Stress Testing and Performance Analysis
A comprehensive set of stress tests was conducted to validate the performance and security features of the Chaos-Lattice model:

- **Decryption Success: True**: The successful decryption indicates that my encryption and decryption algorithms are working cohesively. Encrypted data can be successfully decrypted back to its original form, showing functional correctness.
- **Differential Percentage: 99.3042%**: A high differential percentage between encrypted messages demonstrates that small changes in the input lead to significant changes in the output. This is a desirable feature, as it makes cryptanalysis more difficult.
- **Entropy of Encrypted Messages: 7.7884 and 7.7734 bits**: High entropy values for the encrypted messages indicate that the characters are uniformly distributed. This makes it harder for attackers to find patterns, enhancing security.
- **Estimated Key Entropy: 256.0 bits**: This shows that the key space is vast, making brute-force attacks infeasible. A 256-bit key size is considered secure against current cryptographic attacks.
- **Key Generation Cycles: 9,655,600 cycles**: This measures the computational cost of key generation. While not extremely fast, it's within a range that can be considered practical for many applications.
- **Encryption and Decryption Cycles**: These values (2,276,700 and 1,901,700 cycles, respectively) represent the computational cost for encrypting and decrypting messages. They are acceptable for many use-cases and highlight the efficiency of my encryption scheme.
- **Private Key Entropy: 32,768 bits (approximately)**: This high entropy of the private key further adds to the security of the cryptographic system, making it resilient against attacks that try to predict or guess the key.
- **Entropy of Shared Secret Key: 256.0 bits**: The shared secret key's entropy shows that it's robust and secure, conforming to modern security standards.


## Chaos-Lattice Model in Action
Here's a glimpse of the Chaos-Lattice model:

![2923f594-5512-44f3-b61d-1f5ed332bbe3](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/1ae7e2bf-9c93-4a19-8d19-22e6db28769a)

### Performance Metrics:
- **Key Generation**: 9,655,600 cycles
- **Encryption (Encapsulation)**: 2,276,700 cycles
- **Decryption (Decapsulation)**: 1,901,700 cycles

## Conclusion
The Chaos-Lattice method is not merely a theoretical concept; it is a groundbreaking cryptographic solution designed for the future. By harmonizing the mathematical intricacy of lattice-based cryptography with the unpredictability of chaos maps, we have crafted a system that is both fast and secure. As the quantum era dawns, the Chaos-Lattice method stands as a beacon of innovation, ready to meet new challenges.

## License
MIT



Key Generation Cycles: 9,655,600

Encryption (Encapsulation) Cycles: 2,276,700

Decryption (Decapsulation) Cycles: 1,901,700






 ## Conclusion
The Chaos-Lattice method uniquely combines the mathematical complexity of lattice-based cryptography with the intriguing properties of chaos maps. The lattice part ensures quantum resilience, while the chaos map adds an additional layer of complexity and uniqueness to the encryption process. By carefully integrating these components, the Chaos-Lattice method aims to provide a fast and secure cryptographic system.
## License 
MIT
