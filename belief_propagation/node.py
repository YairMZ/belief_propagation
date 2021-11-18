from __future__ import annotations
import numpy as np
import itertools


class Node:
    _uid_generator = itertools.count()

    def __init__(self, name: str = "") -> None:
        """
        :param name: optional name of node
        """
        self.name = name
        self.uid = next(Node._uid_generator)
        self.neighbors: list[Node] = []
        self.likelihood = None

    def register_neighbor(self, neighbor: Node) -> None:
        self.neighbors.append(neighbor)

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return str(self.uid)

    def get_neighbors(self) -> list[int]:
        return [neighbor.uid for neighbor in self.neighbors]

    def receive_messages(self) -> None:
        pass

    def send_message(self, neighbor_uid: int):
        pass

    def __hash__(self):
        return self.uid


class CNode(Node):

    def update_llr(self):
        pass


class VNode(Node):
    def update_llr(self):
        pass
