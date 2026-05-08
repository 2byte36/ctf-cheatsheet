# Crypto Operator Playbook

## Mindset

Crypto CTFs are usually misuse challenges. Identify the primitive, the parameters, and the attacker capability before attacking. Standard AES/RSA/ECC are not broken; bad modes, bad randomness, bad padding, bad signatures, and bad composition are.

## First-Pass Workflow

1. Strip encodings and containers.
2. Count byte lengths and block sizes.
3. Identify primitive and mode.
4. Identify oracle/query surface.
5. Write a verifier.
6. Attack the weakest assumption.

```bash
rg -a -o '[A-Fa-f0-9]{16,}|[A-Za-z0-9+/=]{20,}' .
rg -a -n 'n *=|e *=|c *=|iv|nonce|salt|mod|signature|hash|sha|aes|rsa|ecdsa'
```

## Primitive Routing

| Clue | Route |
|---|---|
| `n,e,c`, PEM keys, big integers | RSA |
| `r,s,z`, repeated `r` | DSA/ECDSA nonce issues |
| 16-byte block repetition | AES-ECB |
| IV plus block cipher | CBC bit flipping or padding oracle |
| nonce/counter plus XOR-like ciphertext | CTR/stream nonce reuse |
| `hash(secret || msg)` | length extension |
| time seed, `random`, LCG outputs | RNG recovery |
| noisy equations, bounded integers | lattice/Z3/Sage |
| finite fields, curves | ECC/discrete log parameter checks |

## Common Attacks

| Pattern | Attack |
|---|---|
| Single-byte XOR | brute 0..255 and score ASCII |
| Repeating XOR | recover key with known `flag{` or frequency |
| Two-time pad | `c1 xor c2 = p1 xor p2`, crib drag |
| ECB oracle | byte-at-a-time or cut-and-paste |
| CBC admin cookie | flip IV/previous block bits |
| Padding oracle | decrypt block by block |
| CTR nonce reuse | recover keystream with known plaintext |
| RSA small `e` no padding | integer root |
| RSA shared prime | pairwise gcd moduli |
| RSA common modulus | extended gcd combine |
| RSA broadcast | CRT then root |
| RSA close primes | Fermat |
| RSA small `d` | Wiener/continued fractions |
| ECDSA nonce reuse | recover nonce/private key |
| Hash length extension | forge append for Merkle-Damgard hashes |
| LCG | solve state/parameters from outputs |

## Snippets

XOR:

```python
def xor(a,b): return bytes(x ^ y for x,y in zip(a,b))
ct = bytes.fromhex("...")
for k in range(256):
    pt = bytes(c ^ k for c in ct)
    if b"flag{" in pt:
        print(k, pt)
```

RSA integer root:

```python
import gmpy2
from Crypto.Util.number import long_to_bytes
m, exact = gmpy2.iroot(c, e)
if exact:
    print(long_to_bytes(int(m)))
```

Shared prime:

```python
from math import gcd
from Crypto.Util.number import inverse, long_to_bytes
for i,n1 in enumerate(moduli):
    for n2 in moduli[:i]:
        p = gcd(n1, n2)
        if 1 < p < n1:
            q = n1 // p
            d = inverse(e, (p-1)*(q-1))
            print(long_to_bytes(pow(c, d, n1)))
```

CBC bit flip:

```python
def flip(prev_block, old, new, offset):
    b = bytearray(prev_block)
    for i,(o,n) in enumerate(zip(old,new)):
        b[offset+i] ^= o ^ n
    return bytes(b)
```

## Embedded Crypto In Other Categories

The current repository has crypto spread across other folders:

- Web: JWT/JWE, custom MAC, hash length extension, affine OTP, TOTP seed, AES cookie truncation.
- Reverse: SPN/static extraction, XOR, RC4 loaders, lattice/CVP constraints, GF arithmetic, CRT keygens.
- Misc: encoding chains, hash identification, SHA-256 length extension, crypto games, GF(256) Nim.
- Forensics: TLS decryption, weak RSA in PCAPs, ransomware key recovery, C2 crypto.
- Pwn: MD5 preimage gadgets, CRC arbitrary read, XOR keystream write primitives.

## Tools

| Tool | Use |
|---|---|
| PyCryptodome | RSA/AES/hash scripts |
| SageMath | lattices, finite fields, ECC |
| Z3 | bit-vector constraints |
| RsaCtfTool | quick RSA weakness checks |
| OpenSSL | ASN.1/PEM/cert inspection |
| CyberChef | encoding, XOR, quick transforms |
| hash_extender/hashpumpy | length extension |

## Rabbit Holes

- Attacking AES/RSA directly instead of misuse.
- Forgetting encodings/compression before crypto.
- Treating HMAC as length-extension vulnerable.
- Using floating point for big integers.
- Missing endian conversion.
- Ignoring known plaintext like `flag{`, JSON, PNG, ZIP, ASN.1.
- Not testing repeated IV/nonces.

## Sparse Source Coverage

There is no dedicated `ctf-crypto/` source folder yet. This playbook consolidates embedded crypto knowledge and should eventually be split into:

- RSA and number theory
- ECC/signatures
- Symmetric modes
- Hashes/MACs
- RNG
- Lattices
- Oracles
- Encoding/compression boundary

