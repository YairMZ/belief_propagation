from __future__ import annotations
import numpy as np
import itertools
from typing import Any, Callable


class Node:
    _uid_generator = itertools.count()

    def __init__(self, name: str = "") -> None:
        """
        :param name: optional name of node
        """
        self.name = name
        self.uid = next(Node._uid_generator)
        self.neighbors: dict[int, Node] = {}
        self.received_messages: dict[int, Any] = {}  # keys as senders, values as messages
        self.likelihood = None

    def register_neighbor(self, neighbor: Node) -> None:
        self.neighbors[neighbor.uid] = neighbor

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return str(self.uid)

    def get_neighbors(self) -> list[int]:
        return list(self.neighbors.keys())

    def receive_messages(self) -> None:
        for node_id, node in self.neighbors.items():
            self.received_messages[node_id] = node.message(self.uid)

    def message(self, requester_uid: int) -> Any:
        pass

    def __hash__(self):
        return self.uid


class CNode(Node):

    def initialize(self):
        self.received_messages = {node_uid: 0 for node_uid in self.neighbors}

    def message(self, requester_uid: int) -> np.float_:
        def phi(x):
            return -np.log(np.tanh(x/2))
        q = np.array([msg for uid, msg in self.received_messages.items() if uid != requester_uid])
        return np.prod(np.sign(q))*phi(np.sum(phi(q)))


class VNode(Node):
    def __init__(self, channel_model: Callable,name: str = ""):
        """
        :param channel_model: a function which receives channel outputs anr returns relevant message
        :param name: optional name of node
        """
        self.channel_model = channel_model
        self.channel_symbol: int = None  # currently assuming hard channel symbols
        self.channel_llr: np.float_ = None
        super().__init__(name)

    def initialize(self, channel_symbol):
        self.channel_symbol = channel_symbol
        self.channel_llr = self.channel_model(channel_symbol)
        self.received_messages = {node_uid: 0 for node_uid in self.neighbors}

    def message(self, requester_uid: int) -> np.float_:
        return self.channel_llr + np.sum(
            [msg for uid, msg in self.received_messages.items() if uid != requester_uid]
        )

    def llr(self) -> np.float_:
        return self.channel_llr + np.sum(list(self.received_messages.values()))
