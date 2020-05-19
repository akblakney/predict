import numpy as np
from froth import emperical_probability_dist, bins_from_bracket_list,exp_decay_generator
import copy

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

# given: list of daily counts
# returns: 7 x w matrix with A[i] gives ith day count (e.g. A[0] gives Wednesdays)
def transform(ar, period=7):
    # eliminate remainder days
    while len(ar) % period != 0:
        del ar[-1]

    no_weeks = len(ar) // period
    ret = np.zeros((period, no_weeks))
    for i in range(no_weeks):
        for j in range(period):
            ret[j][i] = ar[period * i + j]

    return ret

# returns 7 x iters matrix
def matFromAP(A, P, alpha, iters,period=7):

    # am_pred[i] gives list of N predictions for the next day i
    # e.g. am_pred[1] gives N length list of predictions for next Thursday
    #a, counts = emperical_probability_dist(A[1],1, exp_decay_generator, (alpha),bins=bins, iters = iters)
    am_mat = [emperical_probability_dist(A[i],1, exp_decay_generator, (alpha),bins=bins, iters = iters) for i in range(period)]
    am_mat = np.array([x[1] for x in am_mat])

    pm_mat = [emperical_probability_dist(P[i],1, exp_decay_generator, (alpha),bins=bins, iters = iters) for i in range(period)]
    pm_mat = np.array([x[1] for x in pm_mat])

    # mat is 7 x iters matrix
    return am_mat, pm_mat

def countsFromMat(am_mat, pm_mat,start_am=0, start_pm=0):
    counts = np.array([])
    for iter_no in range(len(am_mat[0])):
        counts = np.append(counts, 0)
        for day in range(len(am_mat)):
            if day >= start_am:
                counts[-1] += am_mat[day][iter_no]
            if day >= start_pm:
                counts[-1] += pm_mat[day][iter_no]
    return counts

A = transform(am)
P = transform(pm)
bracket_list = [190,200,210,220,230,240,250,260]
#bracket_list = [150,160,170,180,190,200,210,220]
bins = bins_from_bracket_list(bracket_list)
iters = 50000
picount = 205
bins = [x - picount for x in bins]

print('picout: ' + str(picount))

for alpha in [.01,.05,.2,]:
    for res in [0,5]:
        temp_bins = copy.copy(bins)
        temp_bins = [x - res for x in temp_bins]
        am_mat, pm_mat = matFromAP(A, P, alpha, iters)
        counts = countsFromMat(am_mat, pm_mat, start_am=6, start_pm=6)

        hist,_ = np.histogram(counts, bins=temp_bins)
        total_pred = hist/iters
        #print(total_pred[3:],alpha,res)
        print('---res, alpha = ' + str(res) + ', ' + str(alpha))
        print('b1 -- b7: ' + str(round(sum(total_pred[:7]),3)) +'                  b8+: ' + str(round(sum(total_pred[7:]),3)))
    print('')

# for alpha in [.001, .01,.05,.2,]:
    
#     am_mat, pm_mat = matFromAP(A, P, alpha, iters)
#     counts = countsFromMat(am_mat, pm_mat, start_am=3, start_pm=4)

#     hist,_ = np.histogram(counts, bins=bins)
#     total_pred = hist/iters
#     print(total_pred,alpha)
