import math
import time
from multiprocessing import Process, Queue

import requests

from expression import Secret, Scalar
from protocol import ProtocolSpec
from test_integration import smc_server, smc_client

FIXED_VAL = 2
CLIENT_NAME_PREFIX = "party_"

FIXED_SCALAR_VAL = 5


def get_comm_cost(comm_type: str):
    url = f"http://localhost:5000/count/bytes/{comm_type}"
    return requests.get(url).content


def run_processes(server_args, *client_args):
    queue = Queue()

    server = Process(target=smc_server, args=(server_args,))
    clients = [Process(target=smc_client, args=(*args, queue)) for args in client_args]

    server.start()
    time.sleep(3)
    for client in clients:
        client.start()

    results = list()
    for client in clients:
        client.join()

    for client in clients:
        results.append(queue.get())

    # get the length of data in communication (send & request)
    request_cost = get_comm_cost("request")
    response_cost = get_comm_cost("response")

    server.terminate()
    server.join()

    time.sleep(2)

    print("Server stopped.")

    return results, request_cost, response_cost


def run(participants, *clients):
    return run_processes(participants, *clients)


def secret_generator(num_party: int) -> dict:
    party_dict = dict()
    for num in range(0, num_party):
        party_dict[CLIENT_NAME_PREFIX + str(num)] = Secret()
    return party_dict


def party_generator(secret_dict):
    parties = dict()
    key_list = secret_dict.keys()
    for key in key_list:
        val = dict()
        val[secret_dict[key]] = FIXED_VAL
        parties[key] = val
    return parties


def expr_generator_add(num_party: int, num_add: int):
    secret_dict = secret_generator(num_party)
    parties = party_generator(secret_dict)
    secret_list = list(secret_dict.values())
    expr = secret_list[0]
    for i in range(0, num_add - 1):
        expr = expr + secret_list[i % num_party]
    return parties, expr


def expr_generator_mul(num_party: int, num_mul: int):
    secret_dict = secret_generator(num_party)
    parties = party_generator(secret_dict)
    secret_list = list(secret_dict.values())
    expr = secret_list[0]
    for i in range(0, num_mul - 1):
        expr = expr * secret_list[i % num_party]
    return parties, expr


def generator_parameters_add(num_party, num_add):
    # generate parties and expr
    parties, expr = expr_generator_add(num_party, num_add)
    prot = ProtocolSpec(expr=expr, participant_ids=list(parties.keys()))
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
    return parties, clients


def generator_parameters_mul(num_party, num_add):
    parties, expr = expr_generator_mul(num_party, num_add)
    prot = ProtocolSpec(expr=expr, participant_ids=list(parties.keys()))
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
    return parties, clients


def generator_local_file(num_party, num_operator, request_cost, response_cost, type):
    file_name = "communication_cost_benchmark.txt"
    with open(file_name, 'a') as f:
        f.write("party_{}_op_{}_type_{}:\n".format(num_party, num_operator, type))
        f.write("   Comm_request_cost: {} bytes\n".format(str(request_cost)[2:-1]))
        f.write("   Comm_response_cost: {} bytes\n".format(str(response_cost)[2:-1]))
        f.write('')


def generator_local_file_with_scalar(num_party, num_operator, num_scalar, request_cost, response_cost, type):
    file_name = "communication_cost_benchmark.txt"
    with open(file_name, 'a') as f:
        f.write("party_{}_op_{}_type_{}_scalar_{}:\n".format(num_party, num_operator, type, num_scalar))
        f.write("   Comm_request_cost: {} bytes\n".format(str(request_cost)[2:-1]))
        f.write("   Comm_response_cost: {} bytes\n".format(str(response_cost)[2:-1]))
        f.write('')


def benchmark_smc_add(num_party, num_operator, benchmark):
    # generate parties， clients
    parties, clients = generator_parameters_add(num_party, num_operator)
    results, request_cost, response_cost = benchmark(run, list(parties.keys()), *clients)
    # results, request_cost, response_cost = run(list(parties.keys()), *clients)
    # generate file that record the cost
    generator_local_file(num_party, num_operator, request_cost, response_cost, "add")
    for res in results:
        assert res == num_operator * FIXED_VAL


def benchmark_smc_mul(num_party, num_operator, benchmark):
    parties, clients = generator_parameters_mul(num_party, num_operator)
    results, request_cost, response_cost = benchmark(run, list(parties.keys()), *clients)
    # results, request_cost, response_cost = run(list(parties.keys()), *clients)
    # generate file that record the cost
    generator_local_file(num_party, num_operator, request_cost, response_cost, "mul")
    for res in results:
        assert res == math.pow(FIXED_VAL, num_operator)


# add scalar  and   multiply scalar
def add_scalar(expr, num_scalar_operator):
    for _ in range(0, num_scalar_operator):
        expr = expr + Scalar(FIXED_SCALAR_VAL)
    return expr


def mul_scalar(expr, num_scalar_operator):
    for _ in range(0, num_scalar_operator):
        expr = expr * Scalar(FIXED_SCALAR_VAL)
    return expr


def generator_parameters_add_scalar(num_party, num_add_operator, num_scalar_operator):
    parties, expr = expr_generator_add(num_party, num_add_operator)
    expr = add_scalar(expr, num_scalar_operator)
    prot = ProtocolSpec(expr=expr, participant_ids=list(parties.keys()))
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
    return parties, clients


def generator_parameters_mul_scalar(num_party, num_add, num_scalar_operator):
    parties, expr = expr_generator_mul(num_party, num_add)
    expr = mul_scalar(expr, num_scalar_operator)
    prot = ProtocolSpec(expr=expr, participant_ids=list(parties.keys()))
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
    return parties, clients

def benchmark_smc_add_scalar(num_party, num_add_operator, num_scalar_operator, benchmark):
    # secret + secret + scalar
    parties, clients = generator_parameters_add_scalar(num_party, num_add_operator, num_scalar_operator)
    results, request_cost, response_cost = benchmark(run, list(parties.keys()), *clients)
    # results, request_cost, response_cost = run(list(parties.keys()), *clients)
    # generate file that record the cost
    generator_local_file_with_scalar(num_party, num_add_operator, num_scalar_operator, request_cost, response_cost,
                                     "add")
    for res in results:
        assert res == FIXED_VAL * num_add_operator + num_scalar_operator * FIXED_SCALAR_VAL


def benchmark_smc_mul_scalar(num_party, num_operator, num_scalar_operator, benchmark):
    # secret * secret * scalar
    parties, clients = generator_parameters_mul_scalar(num_party, num_operator, num_scalar_operator)
    results, request_cost, response_cost = benchmark(run, list(parties.keys()), *clients)
    # results, request_cost, response_cost = run(list(parties.keys()), *clients)
    # generate file that record the cost
    generator_local_file_with_scalar(num_party, num_operator, num_scalar_operator, request_cost, response_cost,
                                     "mul")
    for res in results:
        assert res == math.pow(FIXED_VAL, num_operator) * math.pow(FIXED_SCALAR_VAL, num_scalar_operator)


'''
    for actual report
'''

# increase the number of parties, keep the number of add operations same
def test_actual_party_5_add_50(benchmark):
    benchmark_smc_add(5, 50, benchmark)
def test_actual_party_10_add_50(benchmark):
    benchmark_smc_add(10, 50, benchmark)
def test_actual_party_15_add_50(benchmark):
    benchmark_smc_add(15, 50, benchmark)
def test_actual_party_20_add_50(benchmark):
    benchmark_smc_add(20, 50, benchmark)
def test_actual_party_25_add_50(benchmark):
    benchmark_smc_add(25, 50, benchmark)
def test_actual_party_30_add_50(benchmark):
    benchmark_smc_add(30, 50, benchmark)


# increase the number of parties, keep the number of mul operations same
def test_actual_party_5_mul_10(benchmark):
    benchmark_smc_mul(5, 10, benchmark)
def test_actual_party_10_mul_10(benchmark):
    benchmark_smc_mul(10, 10, benchmark)
def test_actual_party_15_mul_10(benchmark):
    benchmark_smc_mul(15, 10, benchmark)
def test_actual_party_20_mul_10(benchmark):
    benchmark_smc_mul(20, 10, benchmark)
def test_actual_party_25_mul_10(benchmark):
    benchmark_smc_mul(25, 10, benchmark)
def test_actual_party_30_mul_10(benchmark):
    benchmark_smc_mul(30, 10, benchmark)


# increase the number of add operations, keep the number of parties same
def test_actual_party_5_add_10(benchmark):
    benchmark_smc_add(5, 10, benchmark)
def test_actual_party_5_add_50(benchmark):
    benchmark_smc_add(5, 50, benchmark)
def test_actual_party_5_add_100(benchmark):
    benchmark_smc_add(5, 100, benchmark)
def test_actual_party_5_add_200(benchmark):
    benchmark_smc_add(5, 200, benchmark)
def test_actual_party_5_add_300(benchmark):
    benchmark_smc_add(5, 300, benchmark)


# increase the number of scalar in add operations, keep the number of parties and add operation same (addition of scalars)
def test_actual_party_5_add_50_scalar_5(benchmark):
    benchmark_smc_add_scalar(5, 50, 5, benchmark)
def test_actual_party_5_add_50_scalar_10(benchmark):
    benchmark_smc_add_scalar(5, 50, 10, benchmark)
def test_actual_party_5_add_50_scalar_50(benchmark):
    benchmark_smc_add_scalar(5, 50, 50, benchmark)
def test_actual_party_5_add_50_scalar_100(benchmark):
    benchmark_smc_add_scalar(5, 50, 100, benchmark)
def test_actual_party_5_add_50_scalar_200(benchmark):
    benchmark_smc_add_scalar(5, 50, 200, benchmark)


# increase the number of mul operations, keep the number of parties same
def test_actual_party_3_mul_2(benchmark):
    benchmark_smc_mul(3, 2, benchmark)
def test_actual_party_3_mul_4(benchmark):
    benchmark_smc_mul(3, 4, benchmark)
def test_actual_party_3_mul_8(benchmark):
    benchmark_smc_mul(3, 8, benchmark)
def test_actual_party_3_mul_16(benchmark):
    benchmark_smc_mul(3, 16, benchmark)
# def test_actual_party_3_mul_32(benchmark):
#     benchmark_smc_mul(3, 32, benchmark)

# increase the number of scalar in multiplication operations, keep the number of parties and multiplication operation same
def test_actual_party_3_mul_5_scalar_1(benchmark):
    benchmark_smc_mul_scalar(3, 5, 1, benchmark)

def test_actual_party_3_mul_5_scalar_3(benchmark):
    benchmark_smc_mul_scalar(3, 5, 3, benchmark)

def test_actual_party_3_mul_5_scalar_5(benchmark):
    benchmark_smc_mul_scalar(3, 5, 5, benchmark)

def test_actual_party_3_mul_5_scalar_7(benchmark):
    benchmark_smc_mul_scalar(3, 5, 7, benchmark)


# import math
# from asyncio import Queue
# from datetime import time
# from multiprocessing import Process
#
# from expression import Secret, Scalar
# from protocol import ProtocolSpec
# from test_integration import smc_server, smc_client
#
# PREFIX_CLIENT_NAME = 'party_'
# CLIENT_SECRET_VAL = 2
# SCALAR_VAL = 5
#
# def run_processes(server_args, *client_args):
#     queue = Queue()
#
#     server = Process(target=smc_server, args=(server_args,))
#     clients = [Process(target=smc_client, args=(*args, queue)) for args in client_args]
#
#     server.start()
#     time.sleep(3)
#     for client in clients:
#         client.start()
#
#     results = list()
#     for client in clients:
#         client.join()
#
#     for client in clients:
#         results.append(queue.get())
#
#     server.terminate()
#     server.join()
#
#     # To "ensure" the workers are dead.
#     time.sleep(2)
#
#     print("Server stopped.")
#
#     return results
#
#
#
#
# # e.g. client_secret_dict = {
# #         "Alice": alice_secret,
# #         "Bob": bob_secret,
# #         "Charlie": charlie_secret: Secret()
# #     }
# def generate_client_secret_dict(num_clients):
#     client_secret_dict = dict()
#     for i in range(num_clients):
#         client_secret_dict[PREFIX_CLIENT_NAME + str(i)] = Secret()
#     return client_secret_dict
#
#
# # e.g. parties = {
# #         "Alice": {alice_secret: 3},
# #         "Bob": {bob_secret: 14},
# #         "Charlie": {charlie_secret: 2}
# #     }
# def generate_parties(client_secret_dict: dict):
#     parties = dict()
#     for party in client_secret_dict.keys():
#         secret_val_dict = dict()
#         secret_val_dict[client_secret_dict[party]] = CLIENT_SECRET_VAL
#         parties[party] = secret_val_dict
#     return parties
#
#
# def generate_expr_add(num_operators, client_secret_dict):
#     secret_list = [i for i in client_secret_dict.values()]
#     expr = secret_list[0]
#     for index in range(1, num_operators):
#         expr = expr + secret_list[index]
#     return expr
#
#
# def generate_expr_mul(num_operators, client_secret_dict):
#     secret_list = [i for i in client_secret_dict.values()]
#     expr = secret_list[0]
#     for index in range(1, num_operators):
#         expr = expr * secret_list[index]
#     return expr
#
#
# def benchmark_add(num_parties, num_operators, benchmark):
#     client_secret_dict = generate_client_secret_dict(num_parties)
#     parties = generate_parties(client_secret_dict)
#     participants = list(parties.keys())
#     expr = generate_expr_add(num_operators, client_secret_dict)
#     prot = ProtocolSpec(expr=expr, participant_ids=participants)
#     clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
#
#     results = run_processes(participants, *clients)
#
#     expected = num_operators * CLIENT_SECRET_VAL
#
#     for result in results:
#         assert result == expected
#
#
# def benchmark_add_scalar(num_parties, num_operators, num_scalar, benchmark):
#     client_secret_dict = generate_client_secret_dict(num_parties)
#     parties = generate_parties(client_secret_dict)
#     participants = list(parties.keys())
#     expr = generate_expr_add(num_operators, client_secret_dict)
#     for i in range(0, num_scalar):
#         expr += Scalar(SCALAR_VAL)
#     prot = ProtocolSpec(expr=expr, participant_ids=participants)
#     clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
#
#     results = run_processes(participants, *clients)
#
#     expected = num_operators * CLIENT_SECRET_VAL + num_scalar * SCALAR_VAL
#
#     for result in results:
#         assert result == expected
#
#
# def benchmark_mul(num_parties, num_operators, benchmark):
#     client_secret_dict = generate_client_secret_dict(num_parties)
#     parties = generate_parties(client_secret_dict)
#     participants = list(parties.keys())
#     expr = generate_expr_mul(num_operators, client_secret_dict)
#     prot = ProtocolSpec(expr=expr, participant_ids=participants)
#     clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
#
#     results = run_processes(participants, *clients)
#
#     expected = math.pow(CLIENT_SECRET_VAL, num_operators)
#
#     for result in results:
#         assert result == expected
#
#
# def benchmark_mul_scalar(num_parties, num_operators, num_scalar, benchmark):
#     client_secret_dict = generate_client_secret_dict(num_parties)
#     parties = generate_parties(client_secret_dict)
#     participants = list(parties.keys())
#     expr = generate_expr_mul(num_operators, client_secret_dict)
#     for i in range(0, num_scalar):
#         expr = expr * SCALAR_VAL
#     prot = ProtocolSpec(expr=expr, participant_ids=participants)
#     clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
#
#     results = run_processes(participants, *clients)
#
#     expected = math.pow(CLIENT_SECRET_VAL, num_operators) * math.pow(SCALAR_VAL, num_scalar)
#
#     for result in results:
#         assert result == expected
#
#
# def test_add_3party_50operators(benchmark):

