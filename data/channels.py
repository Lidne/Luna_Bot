import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    chan_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    chan_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
