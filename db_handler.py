from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Query
from models import Accounts, Transactions, Balances, Currencies
from config import db_username, db_password
import random
from time import sleep

engine = create_engine(f'postgresql://{db_username}:{db_password}@localhost:5432/atm')

Session = sessionmaker(bind=engine)
session = Session()


def send(amount: float, sender: int, recipient: int):

    try:
        sender_balance = session.query(Balances).filter(Balances.wallet_id == f'{sender}').first()
        sleep(0.5)
        print(f'{sender} is valid')
        recipient_balance = session.query(Balances).filter(Balances.wallet_id == f'{recipient}').first()
        try:
            sleep(0.5)
            print(f'{recipient} is valid')

            if recipient_balance.currency == sender_balance.currency:

                coin = session.query(Currencies).filter(Currencies.id == recipient_balance.currency).first()

                if sender_balance.amount >= amount:

                    # fee

                    fee = amount * 0.001  # 0.1%
                    amount -= fee  # add fee to transaction!!!

                    # transaction

                    session.query(Balances).filter(Balances.id == f'{sender_balance.id}').update(
                        {Balances.amount: Balances.amount - amount},
                        synchronize_session=False)

                    transaction_id = random.randint(99999, 99999999)
                    transaction = Transactions(sender=sender_balance.wallet_id,
                                               recipient=recipient_balance.wallet_id,
                                               transaction_id=transaction_id,
                                               currency=sender_balance.currency,
                                               amount=amount,)
                    session.add(transaction)


                    session.query(Balances).filter(Balances.id == f'{recipient_balance.id}').update(
                        {Balances.amount: Balances.amount + amount},
                        synchronize_session=False)

                    session.commit()

                    sleep(0.5)
                    print(f'Coin is suitable for each of accounts!')
                    sleep(1)
                    print(f'Your account balance {sender_balance.amount} {coin.name}.\n'
                          f'TRANSACTION\'S ID is {transaction_id}')

                else:
                    sleep(0.5)
                    print(f'You don\'t have enough {coin.name}')

            else:
                sleep(0.5)
                print(f'{recipient} account use another coin!')

        except:
            sleep(0.5)
            print(f'{sender} isn\'t valid')

    except:
        sleep(0.5)
        print(f'{recipient} isn\'t valid')


def account_statement(email_or_id):

    if type(email_or_id) == int:
        account = session.query(Accounts).filter(Accounts.id == email_or_id).first()
        balance = session.query(Balances).filter(Balances.account_id == account.id)
        for wallet in balance:
            coin = session.query(Currencies).filter(Currencies.id == wallet.currency).first()
            print(f'{wallet.amount} {coin.name}')
    elif type(email_or_id) == str:
        account = session.query(Accounts).filter(Accounts.email == email_or_id).first()
        balance = session.query(Balances).filter(Balances.account_id == account.id)
        for wallet in balance:
            coin = session.query(Currencies).filter(Currencies.id == wallet.currency).first()
            print(f'{wallet.amount} {coin.name}')
    else:
        print('Something is wrong! Enter your email or account id!')


def my_wallets(email_or_id):

    if type(email_or_id) == int:
        try:
            account = session.query(Accounts).filter(Accounts.id == email_or_id).first()
            balance = session.query(Balances).filter(Balances.account_id == account.id)
            for wallet in balance:
                coin = session.query(Currencies).filter(Currencies.id == wallet.currency).first()
                print(f'{coin.name}\n'
                      f'address: {wallet.wallet_id}')

        except:
            print('We don\'t have user with the same id (or email)!')

    elif type(email_or_id) == str:
        try:
            account = session.query(Accounts).filter(Accounts.email == email_or_id).first()
            balance = session.query(Balances).filter(Balances.account_id == account.id)
            for wallet in balance:
                coin = session.query(Currencies).filter(Currencies.id == wallet.currency).first()
                print(f'{coin.name}\n'
                      f'address: {wallet.wallet_id}')

        except:
            print('We don\'t have user with the same id (or email)!')

    else:
        print('Something\'s wrong!')


def create_wallet(email_or_id, coin):
    the_new = random.randint(99999999, 999999999)
    if type(email_or_id) == int:
        if type(coin) == str:
            coin_id = session.query(Currencies).filter(Currencies.name == coin).first()

            try:
                question = session.query(Balances).filter(Balances.account_id == email_or_id, Balances.currency == coin_id.id).first()
                print(f'You already have wallet for {coin}\n'
                      f'#{question.wallet_id}')

            except:
                try:
                    add = Balances(account_id=email_or_id, wallet_id=the_new, currency=coin_id.id)
                    session.add(add)
                    session.commit()

                    print(f"You just created the new waller for {coin}:\n"
                          f"{the_new}")

                except:
                    print('Incorrect coin!')
        else:
            print('Incorrect coin!')

    elif type(email_or_id) == str:
        if type(coin) == str:
            coin_id = session.query(Currencies).filter(Currencies.name == coin).first()

            try:
                owner_id = session.query(Accounts).filter(Accounts.email == email_or_id).first()
                question = session.query(Balances).filter(Balances.account_id == owner_id.id, Balances.currency == coin_id.id).first()
                print(f'You already have wallet for {coin}\n'
                      f'#{question.wallet_id}')

            except:
                try:
                    owner_id = session.query(Accounts).filter(Accounts.email == email_or_id).first()
                    add = Balances(account_id=owner_id.id, wallet_id=the_new, currency=coin_id.id)
                    session.add(add)
                    session.commit()

                    print(f"You just created the new waller for {coin}:\n"
                          f"{the_new}")

                except:
                    print('Incorrect coin!')
        else:
            print('Incorrect coin!')


def trans_info(id):
    try:
        info = session.query(Transactions).filter(Transactions.transaction_id == id).first()
        coin = session.query(Currencies).filter(Currencies.id == info.currency).first()
        print(f'\ntransaction #{info.transaction_id}\n'
              f'from: {info.sender}\n'
              f'to: {info.recipient}\n'
              f'amount: {info.amount} {coin.name}\n'
              f'date: {info.datetime}')
    except:
        print(f'Wrong transaction number #{id}')


def print_transactions():

    transactions = session.query(Transactions).all()
    for row in transactions:

        print(f'#{row.transaction_id}\n'
              f'{row.sender} -> {row.recipient}\n'
              f'{row.amount} {session.query(Currencies).filter(Currencies.id == row.currency).first().name}\n'
              f'{row.datetime}\n\n')


def wallet_info(wallet):
    num = session.query(Balances).filter(Balances.wallet_id == wallet).first()
    print(f'wallet {wallet}\n'
          f'{num.amount} {session.query(Currencies).filter(Currencies.id == num.currency).first().name}')


""" DEPOSIT """
def deposit(wallet_id, amount):
    session.query(Balances).filter(Balances.wallet_id == wallet_id).update(
        {Balances.amount: amount},
        synchronize_session=False)
    session.commit()