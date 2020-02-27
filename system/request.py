class Request:
    def __init__(self, arr_time, valid=True):
        self.arr_time = arr_time
        self.fin_time = -1
        self.valid = valid

    @property
    def finished(self):
        return self.fin_time > 0

    @property
    def response_time(self):
        if self.finished:
            return max(self.fin_time - self.arr_time, 0)
        else:
            raise Exception("Not finished yet.")

    @property
    def is_valid(self):
        return self.valid