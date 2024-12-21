"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List
import math, random



node_cnt = 0

def verbose_print(s: str, verbose: bool):
    if verbose:
        print(s)

class MCTS_Node(ABC):
    def __init__(self) -> None:
        super().__init__()
        global node_cnt
        self.id = node_cnt
        node_cnt += 1
        self.rollout_id = None

    def set_rollout_id(self, rollout_id: int):
        self.rollout_id = rollout_id

    @abstractmethod
    def find_children(self, rollout_id: int):
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self):
        raise NotImplementedError

    @abstractmethod
    def calculate_reward(self):
        raise NotImplementedError

    @abstractmethod
    def skip_backprop(self):
        raise NotImplementedError

class MCTS_Searcher:
    def __init__(
        self,
        exploration_weight: float,
        weight_scheduler: str,
        num_rollouts: int,
        discount: float,
        verbose: bool = False,
    ):
        self.Q: Dict[MCTS_Node, float] = defaultdict(lambda: 0.0)
        self.N: Dict[MCTS_Node, int] = defaultdict(lambda: 0)
        self.parent2children: Dict[MCTS_Node, List[MCTS_Node]] = dict()

        self.explored_nodes = set()

        self.exploration_weight = exploration_weight
        self.weight_scheduler = weight_scheduler
        self.num_rollouts = num_rollouts
        self.discount = discount

        self.verbose = verbose

        global node_cnt
        node_cnt = 0

    def do_rollout(self, root_node: MCTS_Node, rollout_id: int):
        verbose_print("==> Selecting a node...", self.verbose)
        path_1 = self._select(root_node, rollout_id)
        leaf = path_1[-1]
        verbose_print(f"==> Expanding node {leaf.id}...", self.verbose)
        self._expand(leaf, rollout_id)
        verbose_print(f"==> Simulating node {leaf.id}...", self.verbose)
        path_2 = self._simulate(leaf, rollout_id)
        verbose_print(f"==> Backpropagating...", self.verbose)
        self._backpropagate(path_1 + path_2)
        try:
            return path_2[-1]
        except:
            return path_1[-1]

    def _select(self, node: MCTS_Node, rollout_id: int) -> List[MCTS_Node]:
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            # case 1: a node does not have children, then select the node itself
            if node not in self.parent2children.keys():
                return path

            # case 2: a node has children but not all children have been explored, then randomly select an unexplored child
            # unexplored = set(self.parent2children[node]) - self.explored_nodes   # `set` introduces randomness
            unexplored = [n for n in self.parent2children[node] if n not in self.explored_nodes]
            if unexplored:
                n = random.choice(unexplored)
                path.append(n)
                return path

            # case 3: a node has children and all children have been explored, then select one child and go to the next layer
            node = self._uct_select(node, rollout_id)


    def _expand(self, node: MCTS_Node, rollout_id: int):
        if node in self.explored_nodes:
            return
        if node.is_terminal():
            self.explored_nodes.add(node)
            return
        self.parent2children[node] = node.find_children(rollout_id)

    def _simulate(self, node: MCTS_Node, rollout_id: int) -> List[MCTS_Node]:
        path = []
        cur_node = node
        while True:
            if cur_node.is_terminal():
                self.explored_nodes.add(node)
                return path

            if cur_node not in self.parent2children.keys():
                self.parent2children[cur_node] = cur_node.find_children(rollout_id)

            cur_node = random.choice(self.parent2children[cur_node])
            path.append(cur_node)

    def _backpropagate(self, path: List[MCTS_Node]):
        leaf = path[-1]
        reward = leaf.calculate_reward()
        for node in reversed(path):
            self.Q[node] += reward
            self.N[node] += 1
            self.explored_nodes.add(node)

    def _get_weight(self, rollout_id: int):
        if self.weight_scheduler == "exp":
            return self.exploration_weight * (0.1 ** (rollout_id / self.num_rollouts))
        elif self.weight_scheduler == "lin":
            return self.exploration_weight * (1 - 0.9 * (rollout_id / self.num_rollouts))
        elif self.weight_scheduler == "const":
            return self.exploration_weight

    def _uct_select(self, node: MCTS_Node, rollout_id: int):
        assert all(n in self.explored_nodes for n in self.parent2children[node])
        return max(
            self.parent2children[node], key=lambda n: self._compute_uct(parent_node=node, node=n, rollout_id=rollout_id)
        )

    def _compute_uct(self, parent_node: MCTS_Node, node: MCTS_Node, rollout_id: int):
        if parent_node is None:
            return 666
        else:
            if self.N[node] == 0:
                return 999
            else:
                weight = self._get_weight(rollout_id)
                return self.Q[node] / self.N[node] + weight * math.sqrt(math.log(self.N[parent_node]) / self.N[node])
