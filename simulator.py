from multiprocessing import Process
import numpy as np
import simpy
from system.constants import Par
from trace.trace import gen_reqs
from system.source import Source
from system.vnf import Service, VNF, Instance
from system.server import Server
from system.monitor import Monitor


class Simulator: #(Process):

    def __init__(self, params):
        Process.__init__(self)
        self.env = simpy.Environment()
        self.params = params
        self.monitor = Monitor(params)
        np.random.seed(13)

    def start(self):
        self.run()

    def join(self):
        pass

    def run(self):
        # print(f"Process {self.pid} launched. ({self.params})")

        params = self.params
        config = params.config
        comm_mat = np.array(config.comm_patterns[params.topo])
        server_configs = list(
            zip(config.server_caps, config.server_ucosts))
        servers = [
            Server(self.env, sid, comm_mat, res, ucost) 
            for sid, (res, ucost) in enumerate(server_configs)]
        services = []
        sources = []

        ### Service initialization
        for service_id in range(1, config.num_service+1):
            service_config = config.services[f"NS-{service_id}"]
            service = Service(self.env, service_config)

            gen = gen_reqs(int_len=Par.SLOT_LEN, proc=params.arr_proc)
            src = Source(self.env, gen, service, params.win_size, params.pred)
            src.alpha = params.alpha

            inst_locations = service_config["PLACEMENT"]
            vnf_loc_mapping = list(zip(service.vnfs, inst_locations))

            for vnf, placements in vnf_loc_mapping:
                inst_loc_mapping = list(zip(vnf.instances, placements))
                for inst, loc in inst_loc_mapping:
                    servers[loc-1].host(inst)

            src.outs = service.ingress_vnf.instances
            services.append(service)
            sources.append(src)
        ### End of service initialization.

        all_instances = []
        for s in services:
            for vnf in s.vnfs:
                all_instances += vnf.instances
        
        ### Make the monitor watch every instance
        ### and set default params.
        for inst in all_instances:
            self.monitor.watch(inst)
            inst.params = params

        for server in servers:
            server.params = params
        ### End of setting.

        ### Begin simulation..
        self.env.run(until=config.max_time)
        ### End of simulation.

        ### Printing some results.
        self.monitor.report()
        self.monitor.show_time_stats()
        # self.monitor.save()
        
        # for src in sources:
        #     print(src.max_arr)
