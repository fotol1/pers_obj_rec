from implicit.als import AlternatingLeastSquares as als
from scipy.sparse import csr_matrix
import scipy.sparse as sp
import os
import numpy as np

class BaseRecommender:

    def __init__(self):
        pass

    def score(self,user_id, items_id):
        print(user_id,items_id)
        scores = [self.predict(user_id, item_id) for item_id in items_id]
        return scores

class DumnRecommender(BaseRecommender):
    def __init__(self):
        super(DumnRecommender, self).__init__()

    def predict(self, user_id, item_id):
        return np.random.normal(0,1)

class ALSRecommender(BaseRecommender):

    def __init__(self, factors=32):
        super(ALSRecommender, self).__init__()
        self.model = als(factors=factors)
        os.environ["OPENBLAS_NUM_THREADS"] = '1'
        self.user_factors = None
        self.item_factors = None

    def train(self, rating_matrix,
            user_path='recommenders/als_user_factors',
            item_path='recommenders/als_item_factors'):
        self.model.fit(rating_matrix)
        np.save(user_path, self.model.user_factors)
        np.save(item_path, self.model.item_factors)


    def load(self,
            user_path='recommenders/als_user_factors.npy',
            item_path='recommenders/als_item_factors.npy'):

        self.user_factors = np.load(user_path,allow_pickle=True)
        self.item_factors = np.load(item_path,allow_pickle=True)

    def predict(self, user_id, item_id):

        if self.user_factors is None or self.item_factors is None:
            raise ValueError('The model is not loaded')

        return (self.user_factors[int(user_id)] * self.item_factors[item_id]).sum()
