from branch_bound.rcm import RCM
from copy import deepcopy


class BranchNode:
    def __init__(self, rcm, path):
        super().__init__()
        self.rcm = deepcopy(rcm)
        self.path = deepcopy(path)

    def get_rcm(self):
        return self.rcm

    def get_path(self):
        return self.path

    def get_cost(self):
        return self.rcm.get_cost()
