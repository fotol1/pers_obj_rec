#!flask/bin/python
import os
import unittest
import scipy.sparse as sps
import numpy as np

from recommenders.models import DumnRecommender, ALSRecommender


class TestScoring(unittest.TestCase):
    def setUp(self):

        num_users = 10
        num_items = 10

        num_data = 10
        users = np.random.randint(0, num_users, num_data)
        items = np.random.randint(0, num_items, num_data)
        interactions = np.ones(num_data)

        self.train_matrix = sps.csr_matrix(
            (interactions, (users, items)), shape=(num_users, num_items)
        )

    def test_train_ability(self):

        recommender = ALSRecommender()
        model = recommender.model
        model.fit(self.train_matrix)

        self.assertTrue(isinstance(model.user_factors, np.ndarray))
        self.assertTrue(isinstance(model.item_factors, np.ndarray))

    def test_num_factors(self):

        recommender = ALSRecommender(factors=23)
        model = recommender.model
        model.fit(self.train_matrix)

        self.assertTrue(model.user_factors.shape[1] == 23)
        self.assertTrue(model.item_factors.shape[1] == 23)

        num_users = self.train_matrix.shape[0]
        num_items = self.train_matrix.shape[1]

        self.assertTrue(model.user_factors.shape[0] == num_users)
        self.assertTrue(model.user_factors.shape[0] == num_items)

    def test_single_score_dumn(self):

        model = DumnRecommender()
        user_id = 2
        item_id = 4
        score = model.predict(user_id, item_id)
        self.assertTrue(isinstance(score, float))

    def test_few_scores_dumn(self):

        model = DumnRecommender()
        user_id = 2
        items_id = [4, 2, 5]
        scores = model.score(user_id, items_id)
        self.assertTrue(isinstance(scores, list))

        for score in scores:
            self.assertTrue(isinstance(score, float))
