import re

def parse_nl_query(q: str) -> dict:
    if not q or not q.strip():
        raise ValueError("Empty query")

    s = q.strip().lower()
    filters = {}

    if "palindrom" in s:
        filters["is_palindrome"] = True
    if re.search(r"\b(single|one)\s+word\b", s):
        filters["word_count"] = 1
    m = re.search(r"longer than\s+(\d+)\s+char", s)
    if m:
        filters["min_length"] = int(m.group(1)) + 1
    m = re.search(r"strings?\s+containing\s+the\s+letter\s+([a-z])", s)
    if m:
        filters["contains_character"] = m.group(1)

    if not filters:
        raise ValueError("Unable to parse natural language query")
    return filters
