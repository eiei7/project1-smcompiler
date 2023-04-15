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
    F_p = 3525673

    def __init__(self, val:int, *args, **kwargs):
        # Adapt constructor arguments as you wish
        self.val = val % self.F_p

    def __repr__(self):
        # Helps with debugging.
        return f"Share - {self.val}, {self.F_p}"

    def __add__(self, other):
        if isinstance(other, Share):
            if self.F_p != other.F_p:

                raise ValueError("Shares must have the same finite field.")
            
            return Share((self.val + other.val) % self.F_p)
        else:
            raise TypeError("Only add for Share object")


    def __sub__(self, other):
        if isinstance(other, Share):
            if self.F_p != other.F_p:

                raise ValueError("Shares must have the same finite field.")
            
            return Share((self.val - other.val) % self.F_p)
        else:
            raise TypeError("Only sub for Share object")


    def __mul__(self, other):
        if isinstance(other, Share):
            if self.F_p != other.F_p:

                raise ValueError("Shares must have the same finite field.")
            
            return Share((self.val * other.val) % self.F_p)
        else:
            raise TypeError("Only multiply for Share")


    def serialize(self):
        """Generate a representation suitable for passing in a message."""
        
        return str(self.val)

    @staticmethod
    def deserialize(serialized) -> Share:
        """Restore object from its serialized representation."""

        return Share(int(serialized))


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares."""
    
    if secret >= Share.F_p:
        raise ValueError("Secrect must be less than the finite field.")
    
    # generate (n-1) shares
    shares = [Share(random.randint(0, Share.F_p)) for _ in range(num_shares - 1)] 
    
    # generate the share for the first party in participant_ids list
    share_0 = Share(secret - (sum([share.val for share in shares]) % Share.F_p))

    return [share_0] + shares


def reconstruct_secret(shares: List[Share]) -> int:
    """Reconstruct the secret from shares."""

    if any([share.F_p != shares[0].F_p for share in shares]):

        raise ValueError("All shares must have same finite field inorder to reconstruct secret.")

    return sum([share.val for share in shares]) % (shares[0].F_p)


# Feel free to add as many methods as you want.
