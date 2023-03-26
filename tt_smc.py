from expression import Secret, Scalar
from test_integration import suite

def main():
    """
        f(a, b, c) = (a ∗ b) + (b ∗ c) + (c ∗ a)
        """
    alice_secret = Secret()
    bob_secret = Secret()
    charlie_secret = Secret()

    parties = {
        "Alice": {alice_secret: 3},
        "Bob": {bob_secret: 14},
        "Charlie": {charlie_secret: 2}
    }

    expr = (
            (alice_secret * bob_secret) +
            (bob_secret * charlie_secret) +
            (charlie_secret * alice_secret)
    )
    expected = ((3 * 14) + (14 * 2) + (2 * 3))
    suite(parties, expr, expected)

if __name__ == '__main__':
    main()