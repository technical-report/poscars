import simpy
from system.constants import Par


class Server:
    def __init__(self, env, id, comm_mat, res, ucost):
        self.env = env
        self.id = id
        self.instances = {}
        self.alloc = {}
        self.comm_mat = comm_mat
        self.res = res
        self.ucost = ucost
        self.busy = 0
        self.action = self.env.process(self.run())
        self.params = None

    def run(self):
        while True:
            yield self.env.timeout(Par.SLOT_LEN)
            if self.instances:
                self.schedule()
        
    def unit_comm_cost(self, dest_server):
        return self.comm_mat[self.id, dest_server.id]

    def schedule(self):
        lookup_table = {}

        for inst_id, inst in self.instances.items():
            lookup_table[inst_id] = [
                (y, self.params.V*self.ucost*y - self.params.alpha*inst.q_size*inst.vnf.theta*y) 
                for y in range(self.res+1)
            ]
            
        residual = self.res
        while residual > 0 and len(lookup_table) > 0:
            candidates = [
                [inst_id] + list(min(pairs, key=lambda e: e[1]))
                for inst_id, pairs in lookup_table.items()
            ]
            inst_id, quota, r = min(candidates, key=lambda e: e[2])

            if r > 0:
                break
            else:
                quota = min(quota, residual)
                residual -= quota
                self.alloc[inst_id] = quota
                del lookup_table[inst_id]


    def get_quota(self, instance):
        inst_id = instance.full_id
        if inst_id in self.alloc:
            return self.alloc[inst_id]
        else:
            return 0

    def host(self, instance):
        inst_id = instance.full_id
        if inst_id not in self.instances and instance.server is None:
            self.instances[inst_id] = instance
            instance.server = self
