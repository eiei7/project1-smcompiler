"""
Trusted parameters generator.

MODIFY THIS FILE.
"""

import collections
import math
import random
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

# Feel free to add as many imports as you want.


def get_share(triplet: Tuple, index: int) -> Tuple:
    return triplet[0][index], triplet[1][index], triplet[2][index]


class TrustedParamGenerator:
    """
    A trusted third party that generates random values for the Beaver triplet multiplication scheme.
    """

    def __init__(self):
        self.participant_ids: Set[str] = set()
        # (key) participant_id: (value) index
        self.participant_dict = dict()
        # (key) op_id: (value) triplet
        self.triplet_dict = dict()


    def add_participant(self, participant_id: str) -> None:
        """
        Add a participant.
        """
        self.participant_ids.add(participant_id)
        index = len(self.participant_dict)
        self.participant_dict[participant_id] = index

    def retrieve_share(self, client_id: str, op_id: str) -> Tuple[Share, Share, Share]:
        """
        Retrieve a triplet of shares for a given client_id.
        """
        index = self.participant_dict[client_id]
        if op_id in self.triplet_dict:
            return get_share(self.triplet_dict[op_id], index)

        # generate the a, b, c
        a, b = random.sample(range(0, int(math.floor(math.sqrt(Share.F_P)))), 2)
        c = a * b
        # generate shares of a, b, c for each party
        a_share = share_secret(a, len(self.participant_ids))
        b_share = share_secret(b, len(self.participant_ids))
        c_share = share_secret(c, len(self.participant_ids))
        triplet = (a_share, b_share, c_share)
        # reserve triplet in triplet_dict
        self.triplet_dict[op_id] = triplet
        return get_share(triplet, index)


    # Feel free to add as many methods as you want.
