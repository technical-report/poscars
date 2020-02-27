from util.id_manager import id_manager
from services.vnf import Vnf


class Service:

    def __init__(self, _config):

        self.__id = id_manager.get_next_id("Service")
        self.__data_source = None

        _inst_nums = _config["INST_NUM"]
        self.__theta = _config["THETA"]
        self.__vnfs = [
            Vnf(self, _inst_num, _theta=self.__theta[_vnf])
            for _vnf, _inst_num in enumerate(_inst_nums)
        ]

    def attach_to(self, _ds):
        self.__data_source = _ds

        for _inst in self.ingr_vnf.instances:
            _inst.attach_to(_ds)

    @property
    def id(self):
        return self.__id

    @property
    def chain_len(self):
        return len(self.__vnfs)

    @property
    def vnfs(self):
        return self.__vnfs.copy()

    @property
    def ingr_vnf(self):
        if self.chain_len > 0:
            return self.__vnfs[0]
        else:
            return None

    @property
    def term_vnf(self):
        if self.chain_len > 0:
            return self.__vnfs[-1]
        else:
            return None

    @property
    def non_ingr_vnfs(self):
        return self.__vnfs[1:]

    @property
    def non_term_vnfs(self):
        return self.__vnfs[:-1]

    @property
    def data_source(self):
        return self.__data_source


if __name__ == '__main__':

    from elements.data_source import DataSource as DS

    ds = DS(4, 1)
    service = Service({
        "INST_NUM": [3, 3, 3]
    })
    service.attach_to(ds)

    print(service.vnfs)
    print(service.data_source)
    print(service.ingr_vnf.instances)
    print(service.ingr_vnf.instances[0].data_source)
    print(service.ingr_vnf.queue_backlog_sizes)
    print(service.ingr_vnf.locations)
    print(service.non_ingr_vnfs)
    print(ds.associated_instances)
