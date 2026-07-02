"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import hashlib

MAX_INTEGER = 2147483647


def generate_id(*values: str) -> int:
    """
    Generates a deterministic integer ID using an MD5 hash of the given values.
    The values are concatenated using '&' as a separator before hashing.
    This is used across the domain to ensure idempotency and stable IDs.
    """
    concatenated_value = "&".join(str(v).lower() for v in values)
    aux = hashlib.md5(concatenated_value.encode("utf-8")).hexdigest()
    return int(aux, 16) % MAX_INTEGER
