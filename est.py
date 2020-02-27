import numpy as np
from trace.estimators import DistrEstimator as Estimator1
from trace.estimators import MovingAvgEstimator as Estimator2 
from trace.estimators import EWMAEstimator as Estimator3
from trace.estimators import BBEstimator as Estimator4
from trace.estimators import KalmanEstimator as Estimator5
from trace.estimators import FBEstimator as Estimator6
from trace.trace import gen_reqs


ROUND_NUM = 100000

est1 = Estimator1()
est2 = Estimator2()
est3 = Estimator3()
est4 = Estimator4()
est5 = Estimator5()
est6 = Estimator6()

src = gen_reqs(int_len=0.1)  # in the unit of 10ms
history = [next(src) for _ in range(10)]

est1.feed(history)
est2.feed(history)
est3.feed(history)
est4.feed(history)
est5.feed(history)
est6.feed(history)

errs1 = []
errs2 = []
errs3 = []
errs4 = []
errs5 = []
errs6 = []


for i in range(1, ROUND_NUM):
    new_arrival = next(src)
    
    pred1 = est1.forecast()
    errs1.append(pred1 - new_arrival)
    
    pred2 = est2.forecast()
    errs2.append(pred2 - new_arrival)
    
    pred3 = est3.forecast()
    errs3.append(pred3 - new_arrival)
    
    pred4 = est4.forecast()
    errs4.append(pred4 - new_arrival)
    
    pred5 = est5.forecast()
    errs5.append(pred5 - new_arrival)

    pred6 = est6.forecast()
    errs6.append(pred6 - new_arrival)
    
    est1.feed([new_arrival])
    est2.feed([new_arrival])
    est3.feed([new_arrival])
    est4.feed([new_arrival])
    est5.feed([new_arrival])
    est6.feed([new_arrival])
        
mse = lambda errs: np.average([e**2 for e in errs])
hit = lambda errs: sum([1 for err in errs if err == 0])/ROUND_NUM

perf = hit
print(perf(errs1))
print(perf(errs2))
print(perf(errs3))
print(perf(errs4))
print(perf(errs5))
print(perf(errs6))