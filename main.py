from collections import namedtuple as nt
import numpy as np
import simpy
from simulator import Simulator
from setting.config import ConfigParser as cp


if __name__ == "__main__":
    config = cp.load("setting/setting.yaml")
    Params = nt("Params", [
        "topo", "config", "V", 
        "alpha", "scheme", "arr_proc", 
        "win_size", "pred"])

    sims = []
    for V in config.Vs:
        for win_size in config.win_sizes:
            for pred in config.pred_schemes:
                for scheme in config.schemes:
                    for topo in ["Fat-Tree"]: # ["Fat-Tree"]:
                        for a_proc in ["Trace"]:  #, "Pois"]:
                            p = Params(
                                topo=topo, 
                                config=config, 
                                V=V, 
                                alpha=config.alpha, 
                                scheme=scheme, 
                                arr_proc=a_proc,
                                win_size=win_size,
                                pred=pred  # prediction scheme
                            )
                            sim = Simulator(p)
                            sim.start()
                            sims.append(sim)

    for sim in sims:
        sim.join()