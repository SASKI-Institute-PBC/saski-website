"""Verify the sanitized SASKI Agentic receipt test vector.

Requires: pip install cryptography
Run from the directory containing receipt-sample.json:
    python verify-receipt.py

This example is exact for the published vector, which contains no decimal-number
fields. The complete SASKI canonical encoder converts decimals to fixed
eight-place strings before signing.
"""

import base64
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


PUBLIC_KEY = "uAKiced9sck1tT/LJ82Vw9ouImOqVNYHYn1+STp6MzM="

with open("receipt-sample.json", encoding="utf-8") as receipt_file:
    receipt = json.load(receipt_file)

signature = base64.b64decode(receipt.pop("signature"))
canonical = json.dumps(
    receipt,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")

key = Ed25519PublicKey.from_public_bytes(base64.b64decode(PUBLIC_KEY))
key.verify(signature, canonical)
print("valid")
