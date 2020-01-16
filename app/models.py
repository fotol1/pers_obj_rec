# coding=utf-8
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Представление пользователя сайта в БД.
    Содержит в себе информацию о имени и пароле пользователя
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    interactions = db.relationship("Interaction", backref="user", lazy="dynamic")
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User %r>" % (self.name)

    def set_password(self, password):
        """
        Метод для установки пароля пользователя
        :param password: str. Пароль, введенный пользователем при регистрации
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Метод для проверки введенного пароля с сохраненным хэшом
        :param password: str. Вариант пароля
        :return: bool. True если пароли совпадают, False в противном случае
        """
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Item(db.Model):
    """
    Представление Айтемов в БД. Содержит в себе информацию об имени айтема
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    interactions = db.relationship("Interaction", backref="item", lazy="dynamic")

    def __repr__(self):
        return "<Item %r>" % (self.name)


class Interaction(db.Model):
    """
    Представляет взаимодействия между пользователями и айтемами.
    Хранятся только положительные взаимодействия.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "User id : {}, Item id : {}".format(self.user_id, self.item_id)


class Provider(db.Model):
    """
    Класс, который представляет поставщика айтемов. Экземпляр
    класса представляет из себя сущность, взаимодействуя с которой
    пользователь может потребить айтем. Пример: если объект (айтем) - фильм,
    то провайдер - кинотеатр или сайт с показом фильмов.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Items_in_Provider(db.Model):
    """
    Класс представляет информацию о наличии айтемов в провадерах. В случае
    фильмов экземплярами класса будут пары фильм - кинотеатр. Причем у каждой
    пары есть свой срок действия, так как фильмы могут переставать показываться
    в кинотеатрах, и их надо будет не показывать.
    """

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"))
    valid_from = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    valid_to = db.Column(db.DateTime, index=True)


class Score(db.Model):
    """
    Класс представляет таблицу со скорами для каждой пары пользователь - объект.
    В простом случае у нас имеется одна модель и один скор для каждой пары.
    В качестве масштабирования возможно добавить дату завершения актуальности
    скора и идентификатор модели. На данный момент каждая пара (user_id, item_id)
    имеет вещественное число, которое характеризует степень возможности
    взаимодействия между парой. Чем больше величина, тем более вероятно
    взаимодействие
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    score = db.Column(db.Float)

    def __repr__(self):
        return "Pair (user {},item {}) has a score {}".format(
            self.user_id, self.item_id, self.score
        )
