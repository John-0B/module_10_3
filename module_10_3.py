import random
from time import sleep
from threading import Thread, Lock


class Bank:
    def __init__(self, balance=0):
        lock = Lock()
        self.lock = lock
        self.balance = balance

    def deposit(self):
        for i in range(100):
            number = random.randint(50, 500)
            self.balance += number
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f'Пополнение: {number}. Баланс: {self.balance}.')
            sleep(0.001)

    def take(self):
        for i in range(100):
            number = random.randint(50, 500)
            print(f'Запрос на {number}')
            if number > self.balance:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            if number <= self.balance:
                self.balance -= number
                print(f'Снятие: {number}. Баланс: {self.balance}')
            sleep(0.001)


bk = Bank()
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))
th1.start()
th2.start()
th1.join()
th2.join()
print(f'Итоговый баланс: {bk.balance}')
