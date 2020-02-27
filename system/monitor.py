import numpy as np
import pickle as pk
from matplotlib import pyplot as plt


class Monitor:
    def __init__(self, params):
        self.stats = {
            "comm cost": {},
            "energy cost": {},
            "finished num": {},
            "response time": {},
            "backlog size": {},
        }
        self.attrs = params
    
    def record(self, key, time, val):
        records = self.stats[key]
        if time not in records:
            records[time] = 0
        records[time] += val

    def record_fin(self, reqs):
        reqs = [req for req in reqs if req.is_valid]
        if reqs:
            self.record("finished num", reqs[0].fin_time, len(reqs))
            for req in reqs:
                self.record("response time", req.fin_time, req.response_time)

    def watch(self, inst):
        inst.logger = self

    def report(self):
        print("\n" + "#"*32)

        print(self.attrs)
        print("Average comm. cost:", np.average(list(self.stats["comm cost"].values())))
        print("Average energy cost:", np.average(list(self.stats["energy cost"].values())))
        print("Average queue backlog size:", np.average(list(self.stats["backlog size"].values())))
        
        fin_num = np.sum(list(self.stats["finished num"].values()))
        total_resp_time = np.sum(list(self.stats["response time"].values()))
        if fin_num:
            print("Average response time:", total_resp_time/fin_num)
            print("Finished reqs:", fin_num)

        print("#"*32 + "\n")

    def show_time_stats(self):
        plt.figure(figsize=(20, 8))

        plt.subplot(2, 2, 1)
        plt.title("Communication cost over time")
        time, cost = list(zip(*list(self.stats["comm cost"].items())))
        plt.plot(time, cost, "r-")

        plt.subplot(2, 2, 2)
        plt.title("Energy cost over time")
        time, cost = list(zip(*list(self.stats["energy cost"].items())))
        plt.plot(time, cost, "b-")

        plt.subplot(2, 2, 3)
        plt.title("Total queue backlog size over time")
        time, cost = list(zip(*list(self.stats["backlog size"].items())))
        plt.plot(time, cost, "g-")

        plt.subplot(2, 2, 4)
        plt.title("Finished reqs over time")
        time, cost = list(zip(*list(self.stats["finished num"].items())))
        plt.plot(time, cost, "k-")

        plt.show()

    def save(self):
        attrs = self.attrs
        with open(
            f"data-1205/{attrs.scheme}-{attrs.topo}-{attrs.V}-{attrs.arr_proc}-{attrs.win_size}-{attrs.pred}.p", 
            "wb") as f:
            pk.dump(self.stats, f)

        with open(
            f"logs-1205/{attrs.scheme}-{attrs.topo}-{attrs.V}-{attrs.arr_proc}-{attrs.win_size}-{attrs.pred}.txt", 
            "w+") as f:
            fin_num = np.sum(list(self.stats["finished num"].values()))
            total_resp_time = np.sum(list(self.stats["response time"].values()))
            f.write(
                "\n" + "#"*32 + "\n" + \
                str(self.attrs) + "\n" + \
                "Average comm. cost: %s\n" % (np.average(list(self.stats["comm cost"].values())),) + \
                "Average energy cost: %s\n" % (np.average(list(self.stats["energy cost"].values())),) + \
                "Average queue backlog size: %s\n" % (np.average(list(self.stats["backlog size"].values())),) + \
                (("Average response time: %s\n" % (total_resp_time/fin_num,)) if fin_num else "")  + \
                "Finished reqs: %s\n" % (fin_num,))
