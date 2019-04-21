
class BankAccount:
    def __init__(self, int_rate=0.01, balance=0):
        self.int_rate = int_rate
        self.balance = balance
        
    def deposit(self, amount):
        self.balance += amount
        return self
    def withdraw(self, amount):
        self.balance -= amount
        return self
    def display_account_info(self):
        print(self.balance)
        return self
    def yield_interest(self):
        self.balance += self.balance*0.01
        return self

savings1 = BankAccount(0.05, 300)
savings2 = BankAccount()
savings1.deposit(300).deposit(400).deposit(200).yield_interest().display_account_info()
savings2.deposit(500).deposit(800).withdraw(100).withdraw(200).withdraw(100).yield_interest().display_account_info()


class User:
    def __init__(self, name, email):
       self.name = name
       self.email = email
       self.account = BankAccount(0.02, 0)

    def make_deposit(self, amount):
        self.account.balance += amount
        return self
    def make_withdrawal(self, amount):
        self.account.balance -=amount
        return self
    def display_user_balance(self):
        print(f"{self.name} has $ {self.account.balance} in bank account")
        return self
        
    def transfer_money(self, other_user, amount):
        print(f'{self.name} trabsferring ${amount} to {other_user.name}')
        self.account.balance -=amount
        other_user.account.balance += amount
        return self


david = User('David Brown', 'bd@bank.com')
george = User('George Tomak', 'jt@bank.com')
frank = User('Frank Donnelle', 'fd@bank.com')

david.make_deposit(100).make_deposit(150).make_deposit(200).make_withdrawal(300).display_user_balance()
george.make_deposit(40).make_deposit(400).make_withdrawal(200).make_withdrawal(50).display_user_balance()
frank.make_deposit(788).make_withdrawal(300).make_withdrawal(340).display_user_balance()
george.transfer_money(frank, 50).display_user_balance()
frank.display_user_balance()
