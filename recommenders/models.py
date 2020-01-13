# coding=utf-8
from implicit.als import AlternatingLeastSquares as als
import os
import numpy as np


class BaseRecommender:
    """
    Базовый класс для всех рекомендательных моделей
    """
    def __init__(self):
        pass

    def score(self, user_id, items_id):
        print(user_id, items_id)
        scores = [self.predict(user_id, item_id) for item_id in items_id]
        return scores


class DumnRecommender(BaseRecommender):
    """
    Простейшая модель для рекомендаций. Ранжирует товары для пользователей
    случайным образом
    """
    def __init__(self):
        super(DumnRecommender, self).__init__()

    def predict(self, user_id, item_id):
        """
        Метод возвращает рандомный скор для любой пары
        :param user_id: id пользователя из БД
        :param item_id: id товара из БД
        :return: float: вещественное число от 0 до 1, сформированное
        случайным образом
        """
        return np.random.normal(0, 1)


class ALSRecommender(BaseRecommender):
    """
    Реализация классического метода рекомендаций, описанного в статье
    "Collaborative Filtering for Implicit Feedback Datasets"
    """

    def __init__(self,
                 factors=32,
                 regularization=0,
                 iterations=15,
                 num_threads=1
                 ):
        """
        :param factors: Размерность пространства скрытых представлений
        :param regularization: Коээфициент регуляризации
        :param iterations: Количество итераций
        :param num_threads: Количество процессов
        """
        super(ALSRecommender, self).__init__()
        self.model = als(factors=factors,
                         regularization=regularization,
                         iterations=iterations,
                         num_threads=num_threads)
        os.environ["OPENBLAS_NUM_THREADS"] = '1'
        self.user_factors = None
        self.item_factors = None

    def train(self, rating_matrix,
              user_path='recommenders/als_user_factors',
              item_path='recommenders/als_item_factors'):
        """
        Метод для обучения модели
        :param rating_matrix: scipy.sparse.csr_matrix. Матрица с положительными
        интеракциями между пользователями и айтемами. Содержит implicit (неявный)
        feedback, который известен на текущий момент
        :param user_path: путь для сохранения представлений пользователей
        :param item_path: путь для сохранения представлений айтемов
        """
        self.model.fit(rating_matrix)

        np.save(user_path, self.model.user_factors)
        np.save(item_path, self.model.item_factors)

    def load(self,
             user_path='recommenders/als_user_factors.npy',
             item_path='recommenders/als_item_factors.npy'):
        """
        Метод загружает вектора пользователей и айтемов, выученные моделью.
        Этих векторов достаточно, чтобы получить скоры для всех пар пользователей-товаров
        :param user_path: путь до сохраненных векторов с пользователями
        :param item_path: путь до сохраненных векторов с айтемами
        """
        self.user_factors = np.load(user_path, allow_pickle=True)
        self.item_factors = np.load(item_path, allow_pickle=True)

    def predict(self, user_id, item_id):
        """
        Метод возвращает единственное число (скор) для пары пользователь - айтем.
        БОльший скор соответствует бОльшей уверенности модели в том, что
        подобное взаимодействие возможно
        :param user_id: идентификатор пользователя в БД
        :param item_id: идентификатор айтема в БД
        :return: скор для пары пользователь - айтем
        """
        if self.user_factors is None or self.item_factors is None:
            raise ValueError('The model is not loaded')

        return (self.user_factors[int(user_id)] * self.item_factors[item_id]).sum()
