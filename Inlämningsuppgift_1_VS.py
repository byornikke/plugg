from klasser import *
from datetime import datetime

#startbank()

Customer.add_customer('Niklas Erlandsson', 19960522)
Customer.add_customer('Niklas Erlandsson', 19960522)
Customer.add_customer('Mikael Erlandsson', 19920513)
Customer.add_customer('Pia Boman', 19660325)
Customer.add_customer('Gustav Svensson', 19960809)
Customer.add_customer('Peter Boman', 19730604)
Customer.add_customer('Linus Boman', 20070220)

Account.add_account(19960522)
#Account.add_account(19960522)
#Account.add_account(19920513)

print(*Customer.kunder, sep="\n")

Bank._load()

Account.deposit(19960522,'1001',500)