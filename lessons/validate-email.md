---
title: Validate Email
summary: A reasonable email check in Python — what to do, and what NOT to do.
related: regex, basics, json
---

"Validate an email address" sounds like a one-liner, but it's actually a small philosophy lesson. The RFC that defines email addresses is enormous. The only truly correct validation is "send a confirmation email and see if the user clicks the link." Everything else is a heuristic.

That said, a sensible regex catches 99% of bad input — typos, missing `@`, missing TLD — without rejecting unusual-but-valid addresses.

## A pragmatic check

```python
import re

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
)

def is_valid_email(email: str) -> bool:
    """Return True if `email` looks like a plausible address."""
    if not email or len(email) > 254:    # RFC 5321 length limit
        return False
    return EMAIL_RE.match(email) is not None
```

That regex says: one or more allowed characters, `@`, one or more allowed characters, `.`, and a TLD of at least two letters. It's deliberately conservative.

## Try it

```python
print(is_valid_email("alice@example.com"))       # True
print(is_valid_email("alice+work@gmail.com"))    # True (the + is valid)
print(is_valid_email("no-at-sign.com"))          # False
print(is_valid_email("trailing.dot@x."))         # False
print(is_valid_email(""))                        # False
```

## What this doesn't catch

- **Domains that don't exist.** `alice@asdfgh.qwerty` matches the pattern but no mail server lives there.
- **Disposable / throwaway providers.** If you care, maintain a blocklist.
- **Typos.** `gnail.com`, `outloook.com` — for those, a "did you mean?" suggester is more useful than tighter validation.
- **Unicode addresses.** International domain names use Punycode under the hood; the regex above only covers ASCII.

## When you need more

The `email-validator` PyPI package does DNS lookups and handles international addresses correctly. For most apps, the regex above plus a confirmation email is the right combination — strict enough to catch fat-fingered typos, lenient enough not to reject real customers.

If regex felt magical, [Regular Expressions](/lesson/regex) breaks down what each piece of that pattern means.
