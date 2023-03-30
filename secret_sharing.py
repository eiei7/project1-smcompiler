"""
Secret sharing scheme.
"""

from __future__ import annotations

import random
from typing import List


class Share:
    """
    A secret share in a finite field.
    """

    # Integers modulo a prime p
    F_P = 3525673

    def __init__(self, val, *args, **kwargs):
        # Adapt constructor arguments as you wish
        self.val = val % self.F_P

    def __repr__(self):
        # Helps with debugging.
        return f"Share - {self.val}"

    def __add__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Only add for Share")
        return Share((self.val + other.val) % self.F_P)

    def __sub__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Only sub for Share")
        return Share((self.val - other.val) % self.F_P)

    def __mul__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Only multiply for Share")
        return Share((self.val * other.val) % self.F_P)

    def serialize(self):
        """Generate a representation suitable for passing in a message."""
        return str(self.val)

    @staticmethod
    def deserialize(serialized) -> Share:
        """Restore object from its serialized representation."""
        return Share(int(serialized))


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares."""
    F_P = Share.F_P
    # generate (n-1) shares
    shares_value = random.sample(range(0, F_P), num_shares - 1)
    # generate the share for the first party in participant_ids list
    share_0 = secret - (sum(shares_value) % F_P)
    # generate the list of shares for secret
    shares_value = [share_0] + shares_value

    return [Share(i) for i in shares_value]


def reconstruct_secret(shares: List[Share]) -> int:
    """Reconstruct the secret from shares."""
    return sum(shares, start=Share(0)).val


# Feel free to add as many methods as you want.
