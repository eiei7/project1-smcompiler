"""
Implementation of an SMC client.

MODIFY THIS FILE.
"""
# You might want to import more classes if needed.

import collections
import json
import pickle
from typing import (
    Dict,
    Set,
    Tuple,
    Union
)

from communication import Communication
from expression import (
    Expression,
    Secret, AbstractOperator, Scalar, Addition, Substraction, Multiplication
)
from protocol import ProtocolSpec
from secret_sharing import(
    reconstruct_secret,
    share_secret,
    Share,
)

# Feel free to add as many imports as you want.


class SMCParty:
    """
    A client that executes an SMC protocol to collectively compute a value of an expression together
    with other clients.

    Attributes:
        client_id: Identifier of this client
        server_host: hostname of the server
        server_port: port of the server
        protocol_spec (ProtocolSpec): Protocol specification
        value_dict (dict): Dictionary assigning values to secrets belonging to this client.
        share_dict (dict): Secret() (key) : Share() (value) a Dictionary owned by a party , which contains the
            secret, share pair for this party to compute the expression
    """

    SHARE_PUBLISH_PREFIX = "send_share_from_"
    SHARE_COMPUTATION_RESULT_PREFIX = "computation_result_share_from_"

    def __init__(
            self,
            client_id: str,
            server_host: str,
            server_port: int,
            protocol_spec: ProtocolSpec,
            value_dict: Dict[Secret, int]
        ):
        self.comm = Communication(server_host, server_port, client_id)

        self.client_id = client_id
        self.protocol_spec = protocol_spec
        self.value_dict = value_dict
        self.share_dict = dict()


    def run(self) -> int:
        """
        The method the client use to do the SMC.
        """
        # 1. create shares based on secret and send shares to other parties
        self.create_and_send_share()

        # 2. wait until all parties finished the step 1
        for ids in self.protocol_spec.participant_ids:
            if ids != self.client_id:
                print(f"{self.client_id} retrieve public message from {ids}")
                self.comm.retrieve_public_message(ids, self.SHARE_PUBLISH_PREFIX + ids)

        # 3. process the expression after all parties finished sending shares to each other
        curr_share = self.process_expression(self.protocol_spec.expr)

        # 4. broadcast the local computation result of expression to other parties
        self.comm.publish_message(self.SHARE_COMPUTATION_RESULT_PREFIX + self.client_id, pickle.dumps(curr_share))
        completed_share = [curr_share]

        # 5. retrieve the computation result from other parties
        for ids in self.protocol_spec.participant_ids:
            if ids != self.client_id:
                completed_share.append(
                    pickle.loads(self.comm.retrieve_public_message(ids, self.SHARE_COMPUTATION_RESULT_PREFIX + ids)))

        # 6. reconstruct the secret
        return reconstruct_secret(completed_share)


    # Suggestion: To process expressions, make use of the *visitor pattern* like so:
    def process_expression(
            self,
            expr: Expression
        ):
        if isinstance(expr, Secret):
            return self.get_or_retrieve_share(expr)

        if isinstance(expr, Scalar):
            return Share(expr.value)

        if isinstance(expr, AbstractOperator):
            pre_expr, next_expr = expr.seperate()
            pre_expr_share = self.process_expression(pre_expr)
            next_expr_share = self.process_expression(next_expr)

            if isinstance(expr, Addition) or isinstance(expr, Substraction):
                # case1: both pre_expr and next_expr do not contain Scalar OR
                #        expr is Scalar Additive operation but is_captain = True
                if expr.scalar_format() == 0 or self.is_captain():
                    if isinstance(expr, Addition):
                        return pre_expr_share + next_expr_share
                    elif isinstance(expr, Substraction):
                        return pre_expr_share - next_expr_share

                # case2: expr contain Scalar, is_captain = False
                #        in the other words, parties should not handle the Scalar
                elif expr.scalar_format() == 1:
                    return pre_expr_share
                elif expr.scalar_format() == 2:
                    return next_expr_share
                elif expr.scalar_format() == 3:
                    return Share(0)

            elif isinstance(expr, Multiplication):
                # case1: multiply Scalar
                if expr.scalar_format() > 0:
                    return pre_expr_share * next_expr_share

                # case2: Multiplication using the Beaver triplet protocol




    # Feel free to add as many methods as you want.
    def create_and_send_share(self):
        # 1. generate share list for each secret in SMC_party.value_dict
        for secret in self.value_dict.keys():
            secret_val = self.value_dict[secret]
            num_shares = len(self.protocol_spec.participant_ids)
            # generate the secret shares
            share_list = share_secret(secret_val, num_shares)

            # 2. reserve share in share_dict or send shares to other parties
            for index, ids in enumerate(self.protocol_spec.participant_ids):
                # save in share_dict
                if ids == self.client_id:
                    self.share_dict[secret] = share_list[index]
                # send to others
                else:
                    serialized_share = pickle.dumps(share_list[index])
                    self.comm.send_private_message(receiver_id=ids, label=str(secret.id), message=serialized_share)

            # 3. inform other parties that I already finished the process of creating and sending shares
            self.comm.publish_message(self.SHARE_PUBLISH_PREFIX + self.client_id, "~")

    def get_or_retrieve_share(self, secret: Secret):
        """
            transfer the secret expression to share expression
            if the secret belongs to myself, then get it directly from the local share_dict
            if the secret belongs to other parties, then send retrieve request
        """
        if secret in self.share_dict:
            return self.share_dict[secret]
        else:
            serialized_share = self.comm.retrieve_private_message(str(secret.id))
            share = pickle.loads(serialized_share)
            # record the secret-share pair in local dict share_dict
            self.share_dict[secret] = share
            return share

    def is_captain(self):
        # indicate the first party in the participant list as the captain to process the Addition of a constant operation
        # hence, whether pre_expr or next_expr contain Scalar or not, the captain can handle the add-K operation
        if self.client_id == self.protocol_spec.participant_ids[0]:
            return True
