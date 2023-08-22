# Hybrid Chaos-Lattice Cipher: A Lattice-Based Approach with Chaos Theory

## Introduction
In the era of quantum computing, the landscape of cryptography is rapidly evolving. The Chaos-Lattice method, developed in our lab, is at the forefront of this evolution. This method ingeniously integrates chaos theory with lattice-based cryptography to forge a cryptographic solution that is not only innovative and efficient but also resistant to the threats posed by quantum computing. 

## Methodology

The Chaos-Lattice cryptographic scheme consists of two main components: Chaos Theory and Lattice-Based Cryptography. Here's how these elements are intertwined :

### 1. **Chaos Theory**:
   Chaos theory is leveraged through a combined chaos map that incorporates three variables. The mathematical representation is as follows:

   ![image](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/790f507f-8c57-4595-ad80-124fdbf6ced7)
   
 The chaos map generates pseudorandom values that contribute to the encryption process.

### 2. **Lattice-Based Cryptography**:
   A lattice-based key generation method is employed, given by:

 ![image](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/325db451-0239-47cd-9d59-f3c0a1b7859c)

### 3. **Encryption and Decryption**:
   - **Encryption**:
     The encryption process combines the chaos map with the public key (A, b) and a shared secret key. The chaos map is iteratively applied to each character of the message, and a MAC is computed using HMAC-SHA3.

   - **Decryption**:
     Decryption reverses the encryption process by applying the chaos map in reverse, along with the private key and the shared secret key.



## Stress Testing and Performance Analysis
A comprehensive set of stress tests was conducted to validate the performance and security features of the Chaos-Lattice model:

- **Decryption Success: True**: The successful decryption indicates that my encryption and decryption algorithms are working cohesively. Encrypted data can be successfully decrypted back to its original form, showing functional correctness.
- **Differential Percentage: 99.3042%**: A high differential percentage between encrypted messages demonstrates that small changes in the input lead to significant changes in the output. This makes cryptanalysis more difficult.
- **Entropy of Encrypted Messages: 7.7884 and 7.7734 bits**: High entropy values for the encrypted messages indicate that the characters are uniformly distributed. This makes it harder for attackers to find patterns, enhancing security.
- **Estimated Key Entropy: 256.0 bits**: This shows that the key space is vast, making brute-force attacks infeasible. A 256-bit key size is considered secure against current cryptographic attacks.
- **Key Generation Cycles: 9,655,600 cycles**: This measures the computational cost of key generation.
- **Encryption and Decryption Cycles**: These values (2,276,700 and 1,901,700 cycles, respectively) represent the computational cost for encrypting and decrypting messages.
- **Private Key Entropy: 32,768 bits (approximately)**: This high entropy of the private key further adds to the security of the cryptographic system, making it resilient against attacks that try to predict or guess the key.
- **Entropy of Shared Secret Key: 256.0 bits**: The shared secret key's entropy shows that it's robust and secure, conforming to modern security standards.


## Chaos-Lattice Model in Action
Here's a glimpse of the Chaos-Lattice model:

![image](https://github.com/kylecoding1/hybrid-chaos-theory-cipher-with-a-lattice-based-approach/assets/128002901/563a4a1b-4060-4ac3-8932-92a02a096dc9)

Kyber models : green 

Chaos-Lattice(my model) : red

### Performance Metrics:
- **Key Generation**: 9,655,600 cycles
- **Encryption (Encapsulation)**: 2,276,700 cycles
- **Decryption (Decapsulation)**: 1,901,700 cycles

## Conclusion
The Chaos-Lattice method is a novel cryptographic approach that intertwines the mathematical complexity of lattice-based cryptography with the dynamism of chaos maps. Although currently slower in speed compared to some models like Kyber, the Chaos-Lattice method offers a unique perspective and room for optimization. As work continues on refining and enhancing this method, it stands as an innovative response to the evolving cryptographic landscape.

## License
MIT
