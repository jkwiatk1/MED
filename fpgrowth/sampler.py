import pandas as pd

def sample_transactions():

    path = '../dataset/'
    ts = pd.read_csv('../dataset/transactions_with_parents.csv', header=0)

    sampled = ts.sample(n = 10000)
    sampled.to_csv('%st_10000.csv' % path, index=False)


sample_transactions()



