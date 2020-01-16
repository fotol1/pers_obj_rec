import pandas as pd
import numpy as np
from app import db
from app.models import User, Item, Interaction, Items_in_Provider
from tqdm import tqdm


if __name__ == "__main__":

    Item.query.delete()
    User.query.delete()
    Interaction.query.delete()
    Items_in_Provider.query.delete()
    db.session.commit()

    admin = User(id=0, name="admin")
    admin.set_password("123")
    db.session.add(admin)

    interactions = pd.read_csv("recommenders/u.data", sep="\t", header=None)
    interactions.rename(
        {0: "userId", 1: "itemId", 2: "rating", 3: "timestamp"}, axis=1, inplace=True
    )

    movie_name = pd.read_csv(
        "recommenders/u.item", sep="\t", header=None, encoding="cp1251"
    )
    movie_name["id_name"] = movie_name[0].apply(lambda x: x.split("|")[:2])
    movie_name["id"] = movie_name["id_name"].apply(lambda x: x[0]).astype(int)
    movie_name["name"] = movie_name["id_name"].apply(lambda x: x[1])

    interactions = interactions.merge(movie_name, left_on="itemId", right_on="id")
    interactions = interactions[["userId", "itemId", "name"]]

    possible_names = [
        "Makar",
        "Makariy",
        "Maksim",
        "Marat",
        "Mark",
        "Martin",
        "Matvey",
        "Miron",
        "Miroslav",
    ]

    users_id = list(set(interactions["userId"].values))
    users_name = [
        "{}_{}".format(np.random.choice(possible_names), id) for id in users_id
    ]

    items_id = list(set(interactions["itemId"].values))
    items_name = [
        interactions.loc[interactions["itemId"] == id, "name"].values[0]
        for id in items_id
    ]

    for idx, user_id in tqdm(enumerate(users_id)):
        new_user = User(
            id=int(user_id),
            name=users_name[idx],
            password_hash=str(np.random.randint(0, 100000)),
        )
        db.session.add(new_user)
        db.session.commit()

    for idx, item_id in tqdm(enumerate(items_id)):
        new_item = Item(id=int(item_id), name=items_name[idx])
        db.session.add(new_item)
        db.session.commit()

        """ Определимся, в какой кинотеатр добавить """
        provider_id = np.random.randint(1, 4)
        assert provider_id == 1 or provider_id == 2 or provider_id == 3
        new_note = Items_in_Provider(item_id=int(item_id), provider_id=int(provider_id))
        db.session.add(new_note)

    for userId, itemId in tqdm(interactions[["userId", "itemId"]].values):

        new_interaction = Interaction(user_id=int(userId), item_id=int(itemId))
        db.session.add(new_interaction)

        db.session.commit()
