from froth import emperical_probability_dist, bins_from_bracket_list,exp_decay_generator
import matplotlib.pyplot as plt
import numpy as np


res = 10
am = [
    13,32,7,13,14,5,9,  # 3/11
    11,3,1,6,71,31,23,  # 3/18
    27,1,12,5,20,7,17,  # 3/25
    1,14,2,41,18,14,4, # 4/1
    13,2,45,1,9,4,5, # wed 4/8
    5,2,11,33,11,8,9,   # 4/15
    12,16,15,23,2,4,11, # 4/22
    13,55,12,16,19,6,17,
    6,1,5,9,75,24,32  # 4/29
]

pm = [
    11,15,19,11,13,24,38,  # 3/11
    9,10,57,15,11,12,14,    # 3/18
    4,8,20,22,13,8,9,   # 3/25
    4,5,9,29,5,10,10,   # 4/1
    8,8,33,30,35,12,4,
    6,6,24,22,20,18,9,
    3,17,15,5,42,13,6,
    14,12,18,24,12,4,19,
    3,9,7,18,49,30,16  # 4/15
]

alpha = .05
iters = 10000
bracket_list = [190,200,210,220,230,240,250,260]
bins = bins_from_bracket_list(bracket_list)
bins = [b - (4) for b in bins]
am_steps = 7
pm_steps = 6

for alpha in [.005,.01,.03,.05,.07,.09,.11,.2,.3]:
    am_pred, am_counts = emperical_probability_dist(am, am_steps,exp_decay_generator,(alpha),bins=bins,iters=iters )
    pm_pred, pm_counts = emperical_probability_dist(pm, pm_steps,exp_decay_generator,(alpha),bins=bins,iters=iters )

    total_counts = am_counts + pm_counts

    hist,_ = np.histogram(total_counts, bins=bins)
    total_pred  = hist/iters

    print('alpha',alpha)
    print(total_pred)

