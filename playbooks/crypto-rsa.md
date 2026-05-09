# Crypto RSA

## When to suspect this

- Challenge gives `n`, `e`, `c`, `p`, `q`, `d`, PEM keys, or large decimal/hex integers.
- Multiple ciphertexts/moduli/signatures are provided.
- `e` is small (`3`, `5`, `17`, `65537`) or `n` looks too small.
- Prompt mentions broadcast, common modulus, weak key, prime generation, padding.

## Fast triage checklist

- Parse integers exactly.
- Check bit length of `n`.
- Check if `p`/`q` are given or factorable.
- Check shared factors across moduli.
- Check small `e` no-padding integer root.
- Check common modulus with different exponents.
- Check close primes with Fermat.
- Check small private exponent with Wiener.
- Verify padding format before stripping.

## Manual confirmation

```python
from math import gcd
print(n.bit_length(), e)
print(gcd(n1, n2))
```

Integer root:

```python
import gmpy2
m, exact = gmpy2.iroot(c, e)
print(exact, int(m).to_bytes((m.bit_length()+7)//8,'big')[:50])
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/crypto/rsa_common_checks.py](../scripts/crypto/rsa_common_checks.py) | Quick RSA weakness scan | `python3 scripts/crypto/rsa_common_checks.py --n N --e E --c C` | Root/factor hints |
| [scripts/crypto/rsa_wiener_template.py](../scripts/crypto/rsa_wiener_template.py) | Suspected small `d` | `python3 scripts/crypto/rsa_wiener_template.py N E C` | Decrypted plaintext |
| RsaCtfTool | Broad automated checks | `RsaCtfTool.py -n N -e E --uncipher C` | Factor/decrypt |
| SageMath | Lattice/advanced RSA | `sage solve.sage` | Small-root solution |
| factordb-style lookup | Small known modulus | Paste `n` | Factors |

## Payload starter pack

Checks:

```python
from Crypto.Util.number import long_to_bytes, inverse
from math import gcd

# known p/q
phi = (p-1)*(q-1)
d = inverse(e, phi)
print(long_to_bytes(pow(c,d,n)))

# shared factor
p = gcd(n1,n2)
```

Common modulus:

```python
from gmpy2 import gcdext
g,a,b = gcdext(e1,e2)
m = (pow(c1,int(a),n) * pow(c2,int(b),n)) % n
```

## Exploit skeleton

```python
#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes, inverse
from math import gcd
import gmpy2

n = 0
e = 65537
c = 0

# Try small-exponent root.
m, exact = gmpy2.iroot(c, e)
if exact:
    print(long_to_bytes(int(m)))

# If p and q known:
# p, q = ...
# d = inverse(e, (p-1)*(q-1))
# print(long_to_bytes(pow(c,d,n)))
```

## Escalation path

- If simple checks fail, inspect prime generation code.
- If partial bits of primes are known, use Coppersmith/Sage.
- If padding oracle exists, classify oracle and script queries.
- If multiple related messages exist, test Hastad/broadcast.
- If signatures are involved, test textbook RSA multiplicativity.

## Common bypasses

- Hex vs decimal parsing.
- `bytes_to_long` endian assumptions.
- No padding means many textbook attacks apply.
- Common modulus with negative Bezout coefficient needs modular inverse.
- Close primes make Fermat fast.
- `e=3` and `m^e < n` gives direct root.

## Rabbit holes

- Factoring strong `n` blindly.
- Ignoring multiple moduli relationships.
- Stripping padding incorrectly.
- Using float math for big integers.

## Final solve checklist

- RSA parameters and attack class identified.
- Decryption/signature math verified.
- Plaintext bytes decoded safely.
- Flag format confirmed.
