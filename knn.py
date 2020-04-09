from ts_util import plot
import matplotlib.pyplot as plt

# finds index of nearest neighbor
def find_nn(x, data):
    min_dist = 1000000
    min_index = -1
    for i in range(len(data)):
        if abs(data[i] - x) < min_dist:
            min_dist = abs(data[i] - x)
            min_index = i
    return min_index

def reformat(x):
    assert len(x) % 7 == 0
    i = 0
    ret_x = []
    ret_y = []
    while i + 6 < len(x):
        week = [x[j] for j in range(i, i+7)]
        ret_x.append(week[0])
        ret_y.append(sum(week))
        i += 7
    return ret_x, ret_y

tweets = [24,47,34,30,39,27,42,    # wed 10/30
        17,18,9,82,21,28,19, # wed 11/6
        49,30,37,25,50,15,43,    # wed 11/13
        35,35,28,16,48,21,18,    # wed 11/20
        9,7,1,1,3,36,34,    # wed 11/27 <-- is off?
        41,16,48,20,105,23,39,    # wed 12/4
        77,123,23,25,27,57,21,        # wed 12/11
        70,73,48,6,9,29,12,     # wed 12/18
        13,35,55,14,3,5,54,    # wed 12/25
        15,5,33,6,2,23,19,    # wed 1/1
        1,33,40,14,29,24,21,    # wed 1/8
        26,25,31,25,8,27,5,    # wed 1/15
        142,29,78,71,37,51,36,    # wed 1/22
        29,44,16,56,34,43,29, # wed 1/29      
        36,15,59,72,54,15,47, # wed 2/5
        17,10,23,45,3,18,37, # wed 2/12
        41,33,47,12,13,39,22,   # wed 2/19
        46,11,24,10,29,49,37,   # wed 2/26
        40,31,25,15,4,35,34,    # 3/4
        24,47,26,24,27,29,47,   # 3/11
        20,13,58,21,82,43,37,   # 3/18
        31,9,32,27,31,15,26]    # 3/25

data = []
for i in range(0, len(tweets), 7):
    data.append([tweets[i], sum(tweets[i:i + 7]) / 7])
plot(data,label='wed')

data = []
for i in range(0, len(tweets), 7):
    data.append([(tweets[i] + tweets[i + 1]) / 2, sum(tweets[i:i + 7]) * (1/7)])
plot(data,label='wed and thurs')


# KNN STUFF -----------
x, y = reformat(tweets)
test_index = len(x) - 4
train_x = x[:test_index]
test_x = x[test_index:]
train_y = y[:test_index]
test_y = y[test_index:]

# predict each x in test x
pred = []
for tx in test_x:
    # find closest neighbor
    nn_index = find_nn(tx, train_x)
    pred.append(train_y[nn_index])

print('predicted: ')
print(pred)
print('actual')
print(test_y)




plt.legend()
plt.show()