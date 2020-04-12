from ts_util import tweets_to_bins
from froth import emperical_probability_dist, exp_decay_generator, bins_from_bracket_list
tweets = tweets_to_bins('twitterdata/whitehouse-1586483105',86400)

# use froth
n = 7
alpha = .15
bracket_list = [200,210,220,230,240,250,260,270]
iters = 1000
bins = bins_from_bracket_list(bracket_list)
pred = emperical_probability_dist(tweets, n, exp_decay_generator, (alpha), bins=bins,iters = iters)
print(tweets)
print(pred)