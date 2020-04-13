from froth import emperical_probability_dist, bins_from_bracket_list,exp_decay_generator
import matplotlib.pyplot as plt
import numpy as np


am = [
    13,32,7,13,14,5,9,  # 3/11
    11,3,1,6,71,31,23,  # 3/18
    27,1,12,5,20,7,17,  # 3/25
    1,14,2,41,18,14,4, # 4/1
    13,2,45,1,9 # wed 4/8

]

pm = [
    11,15,19,11,13,24,38,  # 3/11
    9,10,57,15,11,12,14,    # 3/18
    4,8,20,22,13,8,9,   # 3/25
    4,5,9,29,5,10,10,   # 4/1
    8,8,33,30  # 4/8
]

alpha = .05
iters = 1000
bracket_list = [140,150,160,170,180,190,200,210]
bins = bins_from_bracket_list(bracket_list)
bins = [b - (131) for b in bins]
am_steps = 3
pm_steps = 3

am_pred, am_counts = emperical_probability_dist(am, am_steps,exp_decay_generator,(alpha),bins=bins,iters=iters )
pm_pred, pm_counts = emperical_probability_dist(pm, pm_steps,exp_decay_generator,(alpha),bins=bins,iters=iters )

print('len am',len(am_counts))

total_counts = am_counts + pm_counts
print('len total, ', len(total_counts))
print('total counts')
#print(total_counts)

hist,_ = np.histogram(total_counts, bins=bins)
total_pred  = hist/iters

print('am')
print(am_pred)
print('pm')
print(pm_pred)

print('total pred')
print(total_pred)

plt.plot(am)
plt.plot(pm)

plt.show()