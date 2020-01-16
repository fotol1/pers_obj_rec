from recommenders.models import ALSRecommender
from app.models import User, Item, Interaction
from scipy.sparse import csr_matrix


if __name__ == "__main__":

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

    model = ALSRecommender()
    model.train(train_matrix)
