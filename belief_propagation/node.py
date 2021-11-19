from __future__ import annotations
import numpy as np
import itertools
from typing import Any, Callable
from functools import total_ordering
from abc import ABC, abstractmethod


@total_ordering
class Node(ABC):
    """Base class VNodes anc CNodes.
    Derived classes are expected to implement an "initialize" and  method a "message" which should return the message to
    be passed on the graph.
    Nodes are ordered and deemed equal according to their name.
    """
    _uid_generator = itertools.count()

    def __init__(self, name: str) -> None:
        """
        :param name: name of node
        """
        self.name = name
        self.uid = next(Node._uid_generator)
        self.neighbors: dict[int, Node] = {}
        self.received_messages: dict[int, Any] = {}  # keys as senders, values as messages

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

    @abstractmethod
    def message(self, requester_uid: int) -> Any:
        pass

    @abstractmethod
    def initialize(self):
        pass

    def __hash__(self):
        return self.uid

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.name < other.name


class CNode(Node):

    def initialize(self):
        self.received_messages = {node_uid: 0 for node_uid in self.neighbors}

    def message(self, requester_uid: int) -> np.float_:
        def phi(x):
            return -np.log(np.tanh(x/2))
        q = np.array([msg for uid, msg in self.received_messages.items() if uid != requester_uid])
        msg = np.prod(np.sign(q))*phi(np.sum(phi(np.absolute(q))))
        return msg


class VNode(Node):
    def __init__(self, name: str, channel_model: Callable):
        """
        :param name: optional name of node
        :param channel_model: a function which receives channel outputs anr returns relevant message
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

    def estimate(self) -> np.float_:
        return self.channel_llr + np.sum(list(self.received_messages.values()))
