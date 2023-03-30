from expression import Secret
from protocol import ProtocolSpec
from test_integration import run_processes

"""
potential actual use：
    1. Assume a,b,c are restaurants in the mall
    2. they all want to know the total revenue of all the restaurants in the mall in order to evaluate
     whether their own restaurant can continue to achieve good economic benefits in the mall in the next year.
    3. the three restaurants do not want the other restaurants to know their revenue this year.
    4. they decide to use additive SMC protocol to calculate the total revenue of the three restaurants.
    5. total = a_income + b_income + c_income
"""

def test_custom_application():
    business_tom = Secret()
    business_bob = Secret()
    business_alice = Secret()

    tom_income = 156992
    bob_income = 298878
    alice_income = 400000

    expr = business_tom + business_bob + business_alice
    parties = {
        "Tom": {business_tom: tom_income},
        "Bob": {business_bob: bob_income},
        "Alice": {business_alice: alice_income}
    }

    expect_total_income = tom_income + bob_income + alice_income

    participants = list(parties.keys())
    prot = ProtocolSpec(expr=expr, participant_ids=list(parties.keys()))
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
    total_income = run_processes(participants, *clients)
    for income in total_income:
        assert income == expect_total_income