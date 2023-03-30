from asyncio import Queue
from datetime import time
from multiprocessing import Process

import requests

from expression import Secret, Expression
from protocol import ProtocolSpec
from test_integration import run_processes, smc_server, smc_client

SECRET_FIXED_VAL = 2
PARTY_PREFIX = "party_"


def get_comm_cost(comm_type: str):
    url = f"http://localhost/8000/count/bytes/{comm_type}"
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

    # get the bytes produced during the communication
    request_cost = get_comm_cost("request")
    response_cost = get_comm_cost("response")

    server.terminate()
    server.join()

    # To "ensure" the workers are dead.
    time.sleep(2)

    print("Server stopped.")

    return results, request_cost, response_cost

def run(participants, *clients):
    return run_processes(participants, *clients)


def generate_client_secret(party_num: int) -> dict:
    # party_dict k: client_name v: Secret()
    party_dict = dict()
    for client_idx in range(0, party_num):
        party_dict[PARTY_PREFIX + str(client_idx)] = Secret()
    return party_dict


def generate_parties(client_secret_dict: dict) -> dict:
    parties = dict()
    for client_name in list(client_secret_dict.keys()):
        secret_val_dict = dict()
        # secret_val_dict k: Secret()  v: int
        secret_val_dict[client_secret_dict[client_name]] = SECRET_FIXED_VAL
        # parties {client_name: {k Secret(): v int}: dict()}
        parties[client_name] = secret_val_dict
    return parties


def generate_expr_add(num_operator: int, client_secret_dict: dict) -> Expression:
    secret_list = list(client_secret_dict.values())
    expr = secret_list[0]
    for i in range(1, num_operator):
        expr = expr + secret_list[i % len(secret_list)]
    return expr


def run_benchmark(num_party, num_operator, benchmark):
    client_secret_dict = generate_client_secret(num_party)
    parties = generate_parties(client_secret_dict)
    expr = generate_expr_add(num_operator, client_secret_dict)
    participants = list(parties.keys())

    prot = ProtocolSpec(expr=expr, participant_ids=participants)
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]
    results = benchmark(run, participants, *clients)
    # run(participants, *clients)
    for result in results:
        assert result == num_operator * SECRET_FIXED_VAL


def party_3_add_50(benchmark):
    run_benchmark(3, 50, benchmark)