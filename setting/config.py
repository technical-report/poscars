import copy
import yaml


class ConfigParser:

    @staticmethod
    def load(_src_file):
        return ConfigParser(_src_file)

    def __init__(self, src_file):

        _params = None
        if type(src_file) is str:
            with open(src_file, "r") as f:
                _params = yaml.load(f)
        elif hasattr(src_file, "read"):
            _params = yaml.load(src_file)

        self.schemes = _params["SCHEME"]
        self.Vs = _params["VS"]
        self.win_sizes = _params["WIN_SIZES"]
        self.max_time = _params["MAX_SIM_LEN"]
        self.q_policy = _params["Q_POLICYS"]
        self.num_service = _params["NUM_SERVICE"]
        self.num_server = _params["NUM_SERVER"]
        self.comm_patterns = _params["COMM_PATTERNS"]
        self.server_caps = _params["SERVER_CAPS"]
        self.server_ucosts = _params["SERVER_UCOSTS"]
        self.services = _params["SERVICE_CONFIG"]
        self.alpha = _params["ALPHA"]
        self.gamma = _params["GAMMA"]
        self.pred_schemes = _params["PRED_SCHEME"]

        # self.arr_proc = _params["ARRIVAL"]["PROC"]
        # self.total_rate = _params["ARRIVAL"]["TOTAL_RATE"]
        # self.arr_dist = _params["ARRIVAL"]["DIST"]
        # self.d = _params["D"]
        # self.batch_size = _params["BATCH_SIZE"]
        # self.sample_ratio = _params["SAMPLE_RATIO"]
        # self.pred_accs = _params["PRED_ACCS"]
        
        

    def copy(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return "<>"
