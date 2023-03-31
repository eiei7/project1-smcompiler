"""
Trusted parameters generator.

MODIFY THIS FILE.
"""

import collections
from typing import (
    Dict,
    Set,
    Tuple,
)

from communication import Communication
from secret_sharing import(
    share_secret,
    Share,
)

import math
import random

# Feel free to add as many imports as you want.


class TrustedParamGenerator:
    """
    A trusted third party that generates random values for the Beaver triplet multiplication scheme.
    """

    def __init__(self):

        self.participant_ids: Set[str] = set()

        self.triplets: Dict[str, Tuple[Share, Share, Share]] = {}
        
        self.participant_ids_to_index: Dict[str, int] = {} # index:=order


    def add_participant(self, participant_id: str) -> None:
        """
        Add a participant.
        """
        self.participant_ids.add(participant_id)
        
        self.participant_ids_to_index[participant_id] = len(self.participant_ids_to_index)


    def retrieve_share(self, client_id: str, op_id: str) -> Tuple[Share, Share, Share]:
        """
        Retrieve a triplet of shares for a given client_id.
        """
        if client_id not in self.participant_ids:
            raise ValueError(f"{client_id} is not registered.")
        
        idx = self.participant_ids_to_index[client_id]
        
        if op_id in self.triplets:
            a_share, b_share, c_share = self.triplets[op_id]

            return a_share[idx], b_share[idx], c_share[idx]
        
        a, b = random.sample(range(0, int(math.floor(math.sqrt(Share.F_p)))), 2)
        c = a * b

        a_shares = share_secret(a, len(self.participant_ids))
        b_shares = share_secret(b, len(self.participant_ids))
        c_shares = share_secret(c, len(self.participant_ids))
        

        self.triplets[op_id] = (a_shares, b_shares, c_shares)
        
        return a_shares[idx], b_shares[idx], c_shares[idx]
    
    # Feel free to add as many methods as you want.
