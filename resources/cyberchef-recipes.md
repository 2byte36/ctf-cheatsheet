# CyberChef Recipes

## Web Tokens

JWT:

```text
From Base64URL(header) -> JSON Beautify
From Base64URL(payload) -> JSON Beautify
```

Flask/Django cookies:

```text
URL Decode -> Split on . -> From Base64URL -> JSON Beautify
```

## Encoding Chains

Ambiguous hex/base64:

```text
If all chars are 0-9a-f and even length, try From Hex before Base64.
```

Common chain:

```text
URL Decode -> From Base64 -> Gunzip -> Strings
```

## Forensics

Post-carve blob:

```text
Magic -> From Hex -> Detect File Type
```

DNS labels:

```text
Remove dots/suffix -> From Base32 or From Base64 -> Gunzip if starts 1f8b
```

## Crypto

XOR known prefix:

```text
From Hex -> XOR with crib "flag{" -> derive key bytes
```

Two-time pad:

```text
From Hex c1 -> XOR with From Hex c2 -> crib drag
```

## Unicode

UTF-16 endian mojibake:

```text
Encode text UTF-16BE -> Decode UTF-16LE
```

Homoglyph/binary:

```text
Normalize Unicode -> compare codepoints -> map ASCII=0 homoglyph=1
```

