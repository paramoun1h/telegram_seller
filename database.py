from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper,sessionmaker

engine = create_engine('sqlite:///test.db:', echo=True)
Session = sessionmaker(bind=engine)
session=Session()
metadata = MetaData()
users_table = Table('HistoryPaid', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('id_transaktion', String(40)),
                    Column('date', String(40)),
                    Column('total', String(40)),
                    Column('comment', String(40)))
metadata.create_all(engine)


class HistoryOperation:

    def __init__(self, id_transaktion, date, total, comment):
        self.id_transaktion = id_transaktion
        self.date = date
        self.total = total
        self.comment = comment

    def __repr__(self):
        return f"HistoryOperation<{self.id_transaktion},{self.date},{self.total},{self.comment}>"

print (mapper(HistoryOperation, users_table))
element=HistoryOperation('121212','2222','222','31')
session.add(element)
session.commit()
# print(element)
# print(element.comment)