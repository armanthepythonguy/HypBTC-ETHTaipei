import random
import math

# Function to find a random encryption key (public exponent e)
def find_random_enc_key(phi: int) -> int:
    """Generate a random public exponent e coprime with phi."""
    candidates = [3, 5, 7, 11, 13, 17]  # Small common choices for e
    for e in random.sample(candidates, len(candidates)):
        if math.gcd(e, phi) == 1:  # e must be coprime with phi
            return e
    raise ValueError("No suitable e found")

# Function to find decryption key (private exponent d)
def find_dec_key(e: int, phi: int) -> int:
    """Compute private exponent d such that e * d = 1 mod phi."""
    d = pow(e, -1, phi)  # Modular multiplicative inverse
    return d

# Function to generate RSA key pair
def generate_rsa_keys(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """Generate RSA public and private keys from primes p and q."""
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Find encryption key (e)
    e = find_random_enc_key(phi)
    
    # Find decryption key (d)
    d = find_dec_key(e, phi)
    
    return (e, n), (d, n)  # Public key (e, n), Private key (d, n)

# RSA encryption
def rsa_encrypt(plaintext: int, public_key: tuple[int, int]) -> int:
    """Encrypt a plaintext message using the public key."""
    e, n = public_key
    if plaintext >= n:
        raise ValueError("Plaintext must be less than n")
    ciphertext = pow(plaintext, e, n)
    return ciphertext

# RSA decryption
def rsa_decrypt(ciphertext: int, private_key: tuple[int, int]) -> int:
    """Decrypt a ciphertext using the private key."""
    d, n = private_key
    plaintext = pow(ciphertext, d, n)
    return plaintext
