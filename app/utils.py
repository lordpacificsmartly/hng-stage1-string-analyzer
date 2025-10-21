import hashlib
from collections import Counter

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def is_palindrome_casefold(s: str) -> bool:
    t = s.casefold()
    return t == t[::-1]

def word_count(s: str) -> int:
    return len([p for p in s.split() if p])

def character_frequency(s: str) -> dict:
    return dict(Counter(list(s)))

def analyze_string(value: str) -> dict:
    h = sha256_hex(value)
    return {
        "length": len(value),
        "is_palindrome": is_palindrome_casefold(value),
        "unique_characters": len(set(value)),
        "word_count": word_count(value),
        "sha256_hash": h,
        "character_frequency_map": character_frequency(value),
    }