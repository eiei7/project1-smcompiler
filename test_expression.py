"""
Unit tests for expressions.
Testing expressions is not obligatory.

MODIFY THIS FILE.
"""
import unittest
from expression import (Secret, 
                        Scalar,
                        Expression,
                        Addition,
                        Substraction,
                        Multiplication)



class TestExpression(unittest.TestCase):

    # Example test, you can adapt it to your needs.
    def test_expression(self):
        expr1 = Expression()
        expr2 = Expression()

        self.assertNotEqual(expr1.id, expr2.id)

    def test_expr_construction(self):
        a = Secret(1)
        b = Secret(2)
        c = Secret(3)
        expr = (a + b) * c * Scalar(4) + Scalar(3)
        self.assertTrue(repr(expr) == "((Secret(1) + Secret(2)) * Secret(3) * Scalar(4) + Scalar(3))")


if __name__ == '__main__':
    unittest.main()