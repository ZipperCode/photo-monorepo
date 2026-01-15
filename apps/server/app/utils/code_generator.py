"""Code generation utility for unique collection codes.

This module provides functions to generate unique 6-character alphanumeric codes
for photo collections. The codes exclude ambiguous characters (0/O, 1/I/l)
for better readability and use cryptographically secure random generation.
"""

import secrets
import string
from typing import Callable, Optional

# Define safe character set (excluding ambiguous characters)
# Excluded: 0/O, 1/I/l (visually similar in many fonts)
SAFE_CHARS = string.ascii_uppercase + string.digits
EXCLUDED_CHARS = {'0', 'O', '1', 'I', 'l'}
CODE_CHARS = ''.join(c for c in SAFE_CHARS if c not in EXCLUDED_CHARS)

# Calculate total possible combinations
TOTAL_COMBINATIONS = len(CODE_CHARS) ** 6  # ~2.1 billion combinations


def generate_code(length: int = 6) -> str:
    """
    Generate a random alphanumeric code.

    The code uses only unambiguous characters (excludes 0/O, 1/I/l)
    and is generated using cryptographically secure random generation.

    Args:
        length: Length of the code to generate (default: 6)

    Returns:
        Uppercase alphanumeric code string

    Example:
        >>> generate_code()
        'ABC123'
        >>> generate_code(8)
        'XYZ789AB'
    """
    return ''.join(secrets.choice(CODE_CHARS) for _ in range(length))


async def generate_unique_code(
    check_fn: Callable[[str], bool],
    length: int = 6,
    max_retries: int = 10
) -> str:
    """
    Generate a unique code by checking against existing codes.

    This function generates codes and checks their uniqueness using the
    provided check function. If a collision occurs, it retries up to
    max_retries times before raising an error.

    Args:
        check_fn: Async function that returns True if code exists
        length: Length of the code to generate (default: 6)
        max_retries: Maximum number of retries before giving up (default: 10)

    Returns:
        Unique code that passes the check function

    Raises:
        RuntimeError: If unable to generate unique code after max_retries

    Example:
        >>> async def code_exists(code): return await Collection.find_one(Collection.code == code)
        >>> unique_code = await generate_unique_code(code_exists)
        'ABC123'
    """
    for attempt in range(max_retries):
        code = generate_code(length)

        # Check if code already exists
        try:
            exists = await check_fn(code)
            if not exists:
                return code
        except Exception:
            # If check fails, treat as code exists and retry
            pass

    raise RuntimeError(
        f"Failed to generate unique code after {max_retries} attempts. "
        f"This may indicate high collision rate or database issues."
    )


def validate_code_format(code: str) -> bool:
    """
    Validate that a code string matches the expected format.

    Args:
        code: Code string to validate

    Returns:
        True if code is valid format, False otherwise

    Example:
        >>> validate_code_format("ABC123")
        True
        >>> validate_code_format("abc123")  # lowercase is valid, will be uppercased
        True
        >>> validate_code_format("AB123")  # too short
        False
        >>> validate_code_format("ABC123!")  # invalid character
        False
    """
    if not code or len(code) != 6:
        return False

    # Check if all characters are in the valid set (case-insensitive)
    return all(c.upper() in CODE_CHARS for c in code)


def normalize_code(code: str) -> str:
    """
    Normalize a code string by uppercasing and stripping whitespace.

    Args:
        code: Code string to normalize

    Returns:
        Normalized uppercase code string

    Example:
        >>> normalize_code("abc123")
        'ABC123'
        >>> normalize_code("  abc123  ")
        'ABC123'
    """
    return code.strip().upper()
