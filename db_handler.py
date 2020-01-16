from app import app
from app import db
from app.models import User, Item, Interaction
from app.models import Score, Provider, Items_in_Provider
from datetime import datetime
from scipy.sparse import csr_matrix

from recommenders.models import DumnRecommender


class DBHandler:
    def __init__(self):
        pass

    def add_user(self, name, password):
        user = User(name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    def add_item(self, name):
        item = Item(name=name)
        db.session.add(item)
        db.session.commit()

    def add_provider(self, name):
        new_provider = Provider(name=name)
        db.session.add(new_provider)
        db.session.commit()

    def add_interaction(self, user_id, item_id):

        interaction = Interaction.query.filter_by(
            user_id=user_id, item_id=item_id
        ).first()

        if interaction is None:
            new_interaction = Interaction(user_id=user_id, item_id=item_id)
            db.session.add(new_interaction)
            db.session.commit()

    def add_movie_to_provider(
        self, item_id, provider_id, valid_from=None, valid_to=None
    ):

        if valid_from is None:
            valid_from = datetime.utcnow()
        if valid_to is None:
            valid_to = datetime.fromtimestamp(2114380800)

        new_item = Items_in_Provider(
            item_id=item_id,
            provider_id=provider_id,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        db.session.add(new_item)
        db.session.commit()

    def get_train_matrix(self):

        users = User.query.all()
        num_users = max([user.id for user in users]) + 1

        items = Item.query.all()
        num_items = max([item.id for item in items]) + 1

        interactions = Interaction.query.all()
        users_id = [interaction.user_id for interaction in interactions]
        items_id = [interaction.item_id for interaction in interactions]

        data = [1 for i in range(len(users_id))]

        train_matrix = csr_matrix(
            (data, (users_id, items_id)), shape=(num_users, num_items)
        )

        return train_matrix

    def update_scores(self, model):

        users = User.query.all()
        items = Item.query.all()

        for user in users:
            for item in items:
                score = Score(
                    user_id=user.id, item_id=item.id, score=model.score(user, item)
                )

                db.session.add(score)

        db.session.commit()

    def get_all_providers(self):
        return Provider.query.all()

    def get_all_items(self):
        return Item.query.all()

    def get_user_by_name(self, name):
        return User.query.filter_by(name=name).first()

    def get_user_by_id(self, user_id):
        return User.query.filter_by(id=user_id).first()

    def get_provider_by_id(self, id):
        return Provider.query.filter_by(id=id).first()

    def get_interactions_by_id(self, user_id):
        return Interaction.query.filter_by(user_id=user_id).all()

    def get_items_in_provider(self, provider_id):
        return Items_in_Provider.query.filter_by(provider_id=provider_id).all()

    def get_items_by_ids(self, movies_id):
        return Item.query.filter(Item.id.in_(movies_id)).all()


if __name__ == "__main__":
    handler = DBHandler()
    handler.update_scores(DumnRecommender())
