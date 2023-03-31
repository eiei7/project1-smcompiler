"""
Unit tests for the secret sharing scheme.
Testing secret sharing is not obligatory.

MODIFY THIS FILE.
"""

import unittest
import random
from typing import List

from secret_sharing import (Share, 
                            share_secret, 
                            reconstruct_secret)


class ShareTestCase(unittest.TestCase):
    def setUp(self):
        # Create a finite field using NIST P-256 as the prime
        self.modulo = Share.F_p

        # Generate two random secrets
        self.secret1 = random.randint(1, self.modulo - 1)
        self.secret2 = random.randint(1, self.modulo - 1)

        # Gnerate two shares for each secret
        self.share1 = Share(self.secret1)
        self.share2 = Share(self.secret2)

        
    def test_init(self):
        self.assertEqual(self.share1.val, self.secret1 % self.modulo)
        self.assertEqual(self.share1.F_p, self.modulo)

    def test_add(self):
        # Test addition operation
        sum_share = self.share1 + self.share2
        
        excepted = (self.secret1 + self.secret2) % self.modulo

        self.assertEqual(sum_share.val, excepted)


    def test_sub(self):
        # Test subtraction operation
        sub_share = self.share1 - self.share2
 
        excepted = (self.secret1 - self.secret2) % self.modulo

        self.assertEqual(sub_share.val, excepted)


    def test_mul(self):
        # Test multiplication operation
        mul_share = self.share1 * self.share2

        excepted = (self.secret1 * self.secret2) % self.modulo

        self.assertEqual(mul_share.val, excepted)
    

    def test_serial_deserial(self):
        # Test serialization and deserialization
        serialized_share  = self.share1.serialize()
        deserialized_share = Share.deserialize(serialized_share)
        
        self.assertEqual(deserialized_share.val, self.share1.val)


    def test_share_secret_reconstruct_secret(self):
        # Test share secret and reconstruct secret functions
        num_shares = random.randint(2, 10)
        shares = share_secret(self.secret2, num_shares)
        
        self.assertEqual(len(shares), num_shares)

        secret = reconstruct_secret(shares)

        self.assertEqual(secret, self.secret2)



if __name__ == "__main__":
    unittest.main()