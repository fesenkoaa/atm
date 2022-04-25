from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import db_username, db_password
from datetime import datetime

engine = create_engine(f'postgresql://{db_username}:{db_password}@localhost:5432/atm')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Accounts(Base):  # created
    __tablename__ = 'accounts'  # hidden model

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(150))
    email = Column(String(150), unique=True)


class Currencies(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(150))


class Balances(Base):  # created
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True, unique=True)  # hidden
    account_id = Column(Integer, ForeignKey('accounts.id'))  # hidden
    wallet_id = Column(Integer, unique=True)
    currency = Column(Integer, ForeignKey('currencies.id'))
    amount = Column(Numeric())


class Transactions(Base):  # created
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, unique=True)  # hidden
    sender = Column(Integer, ForeignKey('balances.wallet_id'))  # hidden
    recipient = Column(Integer, ForeignKey('balances.wallet_id'))  # hidden
    transaction_id = Column(Integer, unique=True)
    currency = Column(Integer, ForeignKey('currencies.id'))
    amount = Column(Numeric())
    datetime = Column(DateTime(), default=datetime.utcnow)


# class Fees(Base):
#     __tablename__ = 'fees'
#
#     id = Column(Integer, primary_key=True, unique=True)  # hidden
#     transaction_id = Column(Integer, ForeignKey('Transactions'), unique=True)
#     currency = Column(Integer, ForeignKey('currencies.id'))  # hidden
#     amount = Column(Numeric())  # hidden
#     fee = Column(Float)  # 0.01%


# class Assets(Base):
#     __tablename__ = 'assets'  # hidden model, own money
#
#     id = Column(Integer, primary_key=True, unique=True)
#     currency = Column(Integer, ForeignKey('currencies.id'))
#     amount = Column(Numeric())


# Base.metadata.create_all(engine)