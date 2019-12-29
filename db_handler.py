from app import app
from app import db
from app.models import User, Item, Interaction, Score

from recommenders.models import DumnRecommender

class DBHandler:

    def __init__(self):
        pass

    def add_item(self, name):

        item = Item(name=name)
        db.session.add(item)
        db.session.commit()

    def update_scores(self, model):

        users = User.query.all()
        items = Item.query.all()

        for user in users:
            for item in items:
                
                score = Score(user_id = user.id,
                        item_id = item.id,
                        score = model.score(user,item))
                
                db.session.add(score)

        db.session.commit()


if __name__ == '__main__':

    handler = DBHandler()
    handler.update_scores(DumnRecommender())



        
