import copy
from itertools import product
import numpy as np
import csv
import pandas as pd
from scipy.stats import bernoulli
import sys

LOST = -10000000

# shares objects are n x 2 array objects where each tuple gives the
# number of yes and no shares respectively for each bracket
# prices objects are n x 2 array objects where each tuple gives the
# yes and no prices respectively for each bracket
class Market:
    def __init__(self, df):
        self.df = df
        self.df['Avg Price'] = self.df['Avg Price'].str.replace('$', '')
        self.df = self.df.dropna()

        self.types = self.df['Type']#.astype('float')
        self.shares = self.df['Shares'].astype('float')
        self.prices = self.df['Avg Price'].astype('float')
        assert self.prices.size == self.types.size == self.shares.size
        self.n = self.prices.size
        
        
    def market_payout(self, bracket):
        return self.payout(self.shares, self.prices, self.types, bracket)
        

    # return payout if given bracket wins
    def payout(self, shares, prices, types, bracket):
        
        payout = 0
        for i in range(self.n):
            
            # return impossible if payment out of range
            if shares[i] * prices[i] >= 850:
                #print('error: impossible buy (> $850)')
                return LOST
            won = (i == bracket)
            if won:
                # won and have yes
                if types[i] == 'Yes':
                    payout += .9 * (1 - prices[i]) * shares[i]
                # won but have no prices
                elif types[i] == 'No':
                    payout -= prices[i] * shares[i]

            # this bracket lost
            else:
                # lost but have yes prices
                if types[i] == 'Yes':
                    payout -= shares[i] * prices[i]
                elif types[i] == 'No':
                    payout += .9 * (1 - prices[i]) * shares[i]


        return payout

    def risk(self, shares, prices, types):
        payouts = [self.payout(shares, prices, types, x) for x in range(len(shares))]
        return min(payouts)

    # return current market risk
    def market_risk(self):
        return self.risk(self.shares, self.prices, self.types)


    # return cost of buying specified shares at prices
    # shares and prices must be np arrays
    def risk_after_buy(self, shares, prices):
        # shares and prices after buy
        shares = np.array(shares)
        prices  = np.array(prices)
        prev_shares = np.array(self.shares)

        prev_prices = np.array(self.prices)
        s2 = prev_shares + shares
        p2 = np.divide(np.multiply(prev_shares, prev_prices) + np.multiply(shares, prices),
            shares + prev_shares) 

        #return curr_risk - self.risk(s2, p2, self.types)
        return self.risk(s2,p2,self.types)


    # buy given shares and prices (and update shares and prices)
    def buy(self, new_shares, new_prices):
        old_shares = np.array(copy.copy(np.array(self.shares)))
        old_prices = np.array(copy.copy(np.array(self.prices)))

        # update shares and prices
        #print('before buy: ', self.shares)
        self.shares = old_shares + new_shares
        #print('after buy: ', self.shares)
        self.prices = np.divide(np.multiply(old_shares, old_prices) + np.multiply(new_shares, new_prices),
            new_shares + old_shares) 

    # def rangeAdjusted(x):
    #     if x < 1:
    #         return 1
    #     if x 


    # given list of shares, find best one to buy
    def best_shares(self,prev_shares, share_list, prices, max_index=None):
        max_risk = LOST
        max_shares = share_list[0]
        l = len(prev_shares)
        
        
        for shares in share_list:
            # readjust shares to be within range
            shares = [1 if x < 1 else x for x in shares]
            print(shares + self.shares)
            print(self.risk_after_buy(shares, prices))

            if self.risk_after_buy(shares, prices) > max_risk:
                
            
                max_risk = self.risk_after_buy(shares, prices)
                max_shares = shares

        return max_shares, max_risk
    
    # -1, 1, 1 with probabilities given in p
    def best_buy_stochastic(self, prices, max_index=None,iter=10,p=[.33,.33,.34],sell=False):
        prev_shares = copy.copy(np.array(self.shares))
        if max_index is None:
            max_index = len(prices)
      
        shares_list = []
        for _ in range(iter):

            #r = bernoulli.rvs(p, size=max_index)
            r = np.random.randint(low=-1,high=1,size=max_index)
            #print('r is')
            #print(r)
           
            r = np.concatenate((r, np.zeros(len(prev_shares) - max_index)))
            
            #curr_shares = prev_shares + r
            curr_shares = r
            
            #curr_shares = [1 if x < 1 else x for x in curr_shares]
            shares_list.append(curr_shares)        
        
        return self.best_shares(prev_shares, shares_list,prices)


    # returns max shares, and their risk
    # transactions considered:
    #### buy all but one
    #### buy all
    #### buy only one
    #### sell all but one
    #### sell all
    def best_buy(self, prices, max_index=None,sell=True):

        prev_shares = copy.copy(np.array(self.shares))
        #prev_risk = self.market_risk()
        l = len(prev_shares)
        buy_all = prev_shares + np.ones(l)
        shares_list = [buy_all]
        if max_index is None:
            max_index = l
        
        
        if sell:
            sell_all = prev_shares - np.ones(l)
            sell_all = [1 if x < 1 else x for x in sell_all]
            shares_list.append(sell_all)
        for i in range(max_index):
            
            # buy all
            

            # buy all but one
            buy_all_but_one = prev_shares + np.ones(l)
            buy_all_but_one[i] -= 1

            buy_only_one = prev_shares
            buy_only_one[i] += 1

            shares_list.append(buy_all_but_one)
            shares_list.append(buy_only_one)
            
            if sell:

                # sell all but one
                sell_all_but_one = prev_shares - np.ones(l)
                sell_all_but_one[i] += 1
                sell_all_but_one = [1 if x < 1 else x for x in sell_all_but_one]
                shares_list.append(sell_all)
                shares_list.append(sell_all_but_one)

        return self.best_shares(prev_shares, shares_list, prices)

    def iterative_buy(self, prices, max_index=None, iter=10):
        max_shares, max_risk = self.best_buy_stochastic(prices, max_index,p=[0,.5,.5],iter=60)#,sell=True)
        risk0 = self.market_risk()
        #print('risk0')
        #print(risk0)
        while iter > 0:
            # simulate buy
           
            self.buy(max_shares,prices) #- self.shares, prices)
            max_shares, max_risk = self.best_buy_stochastic(prices, max_index,p=[0,.5,.5],iter=60)#,sell=True)
            print('risk: ',max_risk)
            print('shares: ',max_shares)
            print('total: ',self.shares)
            iter -= 1
        print('final shares:', max_shares)

filename = sys.argv[1]

df = pd.read_csv(filename,sep=r'\s*,\s*',engine='python')#index_col='Market Outcome',engine='python')


m = Market(df)
print(m.market_risk())


prices = np.array([.99,.99,.97,.85,.84,.80,.84,.86,.94])
# presprices = np.array([.48,.57,.94,.98,.99,9.940,9.950,9.950,9.69,9.990])
# vpprices = np.array([.80,.8,.86,.9,.94,.94,.95,.95,.98,.97,.98,.99,.98,.98,.98,.99,.99])

print('initial market risk:', m.market_risk())
m.iterative_buy(prices,iter=10)