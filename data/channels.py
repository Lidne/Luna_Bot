import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Channels(SqlAlchemyBase):
    __tablename__ = 'channels'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    chan_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    chan_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    server_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    add_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
