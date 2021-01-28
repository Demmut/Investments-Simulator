import time
import random
import csv

class Wallet:
    
    balance = 1000
    funds = {
        "A1": 0,
        "A2": 0,
        "A3": 0,
        "A4": 0,
        "A5": 0,
    }


class InvestmentSystem:

    file_valuations = open("InvestmentSimulatorAnalysis/data.csv", 'w')
    file_wallet = open("InvestmentSimulatorAnalysis/wallet.csv", 'w')
    writer_valuations = csv.writer(file_valuations)
    writer_wallet = csv.writer(file_wallet)
    writer_valuations.writerow(["A1","A2","A3","A4","A5"])
    writer_wallet.writerow(["A1","A2","A3","A4","A5","Balance","Total"])

    funds = {
        "A1": 100,
        "A2": 100,
        "A3": 100,
        "A4": 100,
        "A5": 100,
    }

    fluct = {
        "A1": [random.uniform(-0.5, 0), random.uniform(0, 0.5)],
        "A2": [random.uniform(-0.5, 0), random.uniform(0, 0.5)],
        "A3": [random.uniform(-0.5, 0), random.uniform(0, 0.5)],
        "A4": [random.uniform(-0.5, 0), random.uniform(0, 0.5)],
        "A5": [random.uniform(-0.5, 0), random.uniform(0, 0.5)],
    }

    start = True
    stime = time.time()
    time_passed = 0

    def buy(self, fund, unit, wallet):
        price = self.funds[fund]*unit
        if wallet.balance >= price:
            wallet.funds[fund] += unit
            wallet.balance -= price
        
    def sell(self, fund, unit, wallet):
        price = self.funds[fund]*unit
        if wallet.funds[fund] >= unit:
            wallet.funds[fund] -= unit
            wallet.balance += price
        
    def ViewOptions (self, wallet):
        total = 0
        print("Balance: " + str(wallet.balance))

        for fund in wallet.funds:
            price = self.funds[fund]*wallet.funds[fund]
            total += self.funds[fund]*wallet.funds[fund]
            print("Fund " + fund + ": Amount = " + str(wallet.funds[fund]) + "\tPrice: " + str(price))
        
        total += wallet.balance
        print("Total: " + str(total))

    def valuation(self, count):
        if (count > 0):
            for fund in self.funds:
                self.funds[fund] += random.uniform(self.fluct[fund][0], self.fluct[fund][1])
            count -= 1
            self.writer_valuations.writerow(list(self.funds.values()))
            self.valuation(count)

    def run(self, wallet):
        delta_time = int(time.time() - self.stime)
        if delta_time > 0:
            self.stime = time.time()
            self.valuation(delta_time)
        if self.start:
            print("Action options: ")
            print("Buy  - (eg. B A1 4)")
            print("Sell - (eg. S A3 2): ")
            print("View - To view balance options")
            print("Exit - Exit the application")
            self.start = False
        
        inp = input(">>> ")
        tokens = inp.split(" ")
        

        if tokens[0] == "View":
            self.ViewOptions(wallet)
        elif tokens[0] == "B":
            if tokens[1] in self.funds:
                self.buy(tokens[1], int(tokens[2]), wallet)
        elif tokens[0] == "S":
            if tokens[1] in self.funds:
                self.sell(tokens[1], int(tokens[2]), wallet)
        elif tokens[0] == "Exit":
            self.start = True
            return

        self.run(wallet)

    def total_wallet(self, wallet):
        total = 0
        for fund in wallet.funds:
            total += self.funds[fund]*wallet.funds[fund]
        total += wallet.balance
        return total

    def auto_run(self, wallet, count):

        for i in range(count):
            f = random.choice(list(self.funds.keys()))

            if random.choice([True, False]):
                print("Buy " + f)
                self.buy(f, 1, wallet)
            else:
                self.sell(f, 1, wallet)
                print("Sell " + f)
            arr = list(wallet.funds.values())
            arr.append(wallet.balance)
            arr.append(self.total_wallet(wallet))
            self.writer_wallet.writerow(arr)
            if random.choice([True, False]):
                self.valuation(1)
        print("Total delta of money through the system usage: ")
        print("Initial: 1000")
        print("Final: " + str(self.total_wallet(wallet)))

if __name__ == "__main__":

    c = input("Simulation or test (s/t): ")
    x = int(input("How many times the system should run? : "))
    wallet = Wallet()
    system = InvestmentSystem()
    if c == 's':
        system.auto_run(wallet, x)
    elif c == 't':
        system.run(wallet)
