from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.sql import exists

Base = declarative_base()


class History(Base):
    __tablename__ = 'HistoryPaid'
    id = Column(Integer, primary_key=True)
    date = Column(String(40), nullable=False)
    total = Column(Integer, nullable=False)
    comment = Column(String(40), nullable=False)

    def __str__(self):
        return f'{self.date},{self.total},{self.comment}'


class Operation:
    def __init__(self):
        engine = create_engine('sqlite:///sqlalchemy_example.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        DBSession = scoped_session(sessionmaker(bind=engine))
        self.session = DBSession()

    def select(self, comment, date):
        result = self.session.query(History).filter(History.comment == comment,
                                                    History.date == date).first()
        return result

    def commit(self, comment, date):

        result = self.session.query(
            exists().where(History.comment == comment)).scalar()
        if result == True:
            elements = self.session.query(History).filter(History.comment == comment).first()
            elements.date = date
            elements.total += 100
            self.session.commit()
        else:
            newHistory = History(date=date, total=100, comment=comment)
            self.session.add(newHistory)
        self.session.commit()
