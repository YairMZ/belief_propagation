from .graph import TannerGraph
from numpy.typing import ArrayLike, NDArray
import numpy as np


class BeliefPropagation:
    def __init__(self, graph: TannerGraph, h: ArrayLike, max_iter: int):
        self.h = np.array(h)
        self.graph = graph
        self.n = len(graph.v_nodes)
        self.max_iter = max_iter

    def decode(self, channel_word) -> tuple[NDArray, NDArray, bool]:
        if len(channel_word) != self.n:
            raise ValueError("incorrect block size")

        # initial step
        for idx, node in enumerate(self.graph.ordered_v_nodes()):
            node.initialize(channel_word[idx])
        for node in self.graph.c_nodes.values():  # send initial channel based messages to check nodes
            node.receive_messages()

        for _ in range(self.max_iter):
            # Check to Variable Node Step(horizontal step):
            for node in self.graph.v_nodes.values():
                node.receive_messages()
            # Variable to Check Node Step(vertical step)
            for node in self.graph.c_nodes.values():
                node.receive_messages()

            # Check stop condition
            llr = np.array([node.estimate() for node in self.graph.ordered_v_nodes()])
            estimate = np.array([1 if node_llr < 0 else 0 for node_llr in llr])
            syndrome = self.h.dot(estimate) % 2
            if not syndrome.any():
                break

        return estimate, llr, not syndrome.any()
