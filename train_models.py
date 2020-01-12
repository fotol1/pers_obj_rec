from db_handler import DBHandler
from recommenders.models import ALSRecommender

if __name__ == '__main__':

    db_handler = DBHandler()

    train_matrix = db_handler.get_train_matrix() 

    model = ALSRecommender()
    model.train(train_matrix)
