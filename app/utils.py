from app.models import User, Interaction, Item
from config import CURRENT_USER_FACTORS_PATH
from db_handler import DBHandler

import numpy as np


def find_negative_item(user_id):

    db_handler = DBHandler()

    all_items = db_handler.get_all_items()
    items_ids = [item.id for item in all_items]

    interacted_items = db_handler.get_interactions_by_id(user_id=user_id)
    interacted_items_id = [item.item_id for item in interacted_items]
    not_interacted_items_id = list(set(items_ids) - set(interacted_items_id))
    not_interacted_items = db_handler.get_items_by_ids(not_interacted_items_id)

    if not_interacted_items is None:
        return None
    else:
        not_interacted_item = np.random.choice(not_interacted_items)
        return not_interacted_item


def find_similar_user(user_id):

    db_handler = DBHandler()

    user_factors = np.load(CURRENT_USER_FACTORS_PATH, allow_pickle=True)

    if user_id > user_factors.shape[0]:
        most_similar_user_id = np.random.choice(user_factors.shape[0])
    else:
        user_factor = user_factors[user_id - 1]
        dot_product = (user_factor * user_factors).sum(1)
        indexes = np.argsort(dot_product)[::-1]
        most_similar_user_id = int(indexes[-2])

    print(most_similar_user_id, type(most_similar_user_id))
    most_similar_user = db_handler.get_user_by_id(user_id=most_similar_user_id)
    return most_similar_user
