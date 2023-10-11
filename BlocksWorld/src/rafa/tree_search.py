import numpy as np
from abc import ABC
from copy import deepcopy
from typing import List, Tuple


class AbsNode(ABC): pass


class TreeSearch:
    def __init__(self,
                 search_depth: int,
                 sample_per_node: int,
                 sampler: str='heuristic',
                 discount: float=1) -> None:
        '''
        sampler in {heuristic, random}
        '''
        self.search_depth = search_depth
        self.sample_per_node = sample_per_node
        if sampler == 'heuristic':
            self.sampler = self.heuristic_sampler
        elif sampler == 'random':
            self.sampler = self.random_sampler
        else:
            raise NotImplementedError
        self.discount = discount

    def heuristic_sampler(self, node: AbsNode) -> List[AbsNode]:
        children = node.get_children()
        children.sort(reverse=True, key=lambda x: x._prob_r*x._alpha+x._v_rand)
        print('sorted', [(child._prob_r, child._alpha, child._v_rand) for child in children])
        return children[:self.sample_per_node]\
            if self.sample_per_node != 0 else children

    def epsgreedy_sampler(self, node: AbsNode) -> List[AbsNode]:
        children = node.get_children()
        children.sort(reverse=True, key=lambda x: x._prob_r*x._alpha+x._v_rand)

    def random_sampler(self, node: AbsNode) -> List[AbsNode]:
        children = node.get_children()
        weights = np.array([child._prob_r*child._alpha+child._v_rand for child in children])
        weights /= np.sum(weights)
        return np.random.choice(
            children,
            size=min(len(children), self.sample_per_node),
            replace=False,
            p=weights
        )\
            if self.sample_per_node != 0 else children

    def __call__(self, father_node: AbsNode) -> Tuple[AbsNode, int]:
        paths = []
        returns = []
        def route(node: AbsNode, path: List[AbsNode]) -> None:
            if node.depth - father_node.depth >= self.search_depth or node.is_terminal:
                paths.append(path)
                # compute cumulative rewards
                c_rwd = 0
                for s in path:
                    c_rwd = c_rwd * self.discount + s._prob_r*s._alpha
                returns.append(c_rwd + node._v_rand)
            else:
                print('father state', node.prompt)
                children_sample = self.sampler(node)
                for new_node in children_sample:
                    print('children state', new_node.prompt)
                    tmp_path = deepcopy(path)
                    tmp_path.append(new_node)
                    route(new_node, tmp_path)
        # recursively generate feasible plans
        route(father_node, [])
        # find the approximately best plan
        max_id = np.argmax(returns)
        # only take one actual step
        next_node = paths[max_id][0]
        assert next_node.depth == father_node.depth + 1
        return next_node
