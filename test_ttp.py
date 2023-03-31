"""
Unit tests for the trusted parameter generator.
Testing ttp is not obligatory.

MODIFY THIS FILE.
"""
import unittest
from typing import Dict, Tuple

from ttp import TrustedParamGenerator
from secret_sharing import Share


class TestTrustedParamGenerator(unittest.TestCase):

    def test_add_participant(self):
        generator = TrustedParamGenerator()

        generator.add_participant("Alice")
        generator.add_participant("Bob")
        
        self.assertEqual(len(generator.participant_ids), 2)

    def test_retrieve_share(self):
        generator = TrustedParamGenerator()

        generator.add_participant("Alice")
        generator.add_participant("Bob")

        # retrieve shares for Alice
        share1, share2, share3 = generator.retrieve_share("Alice", "opa")

        self.assertIsInstance(share1, Share)
        self.assertIsInstance(share2, Share)
        self.assertIsInstance(share3, Share)

        # retrieve shares for Bob
        share4, share5, share6 = generator.retrieve_share("Bob", "opb")

        self.assertIsInstance(share4, Share)
        self.assertIsInstance(share5, Share)
        self.assertIsInstance(share6, Share)



