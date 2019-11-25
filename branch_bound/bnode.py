from branch_bound.rcm import RCM


class BranchNode:
    def __init__(self, rcm, path, identity):
        self.id = identity
        self.rcm = rcm
        self.path = path

    def get_rcm(self):
        return self.rcm

    def get_path(self):
        return self.path

    def get_cost(self):
        return self.rcm.get_cost()

    def get_id(self):
        return self.id
