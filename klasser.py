from datetime import datetime
import numpy as np

def startbank():

    menu.openmenu()
    return

class Bank():
    kundinfo = []
    def _load():
        
        with open("mockdata.txt", "r") as file:
            data = [line.strip() for line in file]
            
        #print(Bank.kundinfo)
            for line in data:
                line = line.replace("#", ":")
                Bank.kundinfo.append(line.split(":"))
                #print(line.split(':'))
                        
        return Bank.kundinfo

    def get_customers(): 
        kundlista = []
        for e in Bank.kundinfo:
            kundlista.append(e[2:0:-1])
        print(*kundlista, sep="\n")
        return 

    
    pass

class Customer():
    #Bank.kundinfo = [] # BIG LIST INFO - här är allt. Vet inget bättre sätt
    def add_customer(name, pnr):
        datum = datetime.now().strftime("%Y%m%d") 
        if int(datum) - int(pnr) < 180000: #differens mellan dagens datum och födelsedatum. <180000 blir minderårig
            return print("Kund under 18."), False
        l = len(Bank.kundinfo) + 1
    
        if any([e[2] == pnr for e in Bank.kundinfo]): # kollar så inte pnr redan finns i kundlistan
            return print("Kund: ",name," finns redan."), False
        
        ID = Customer.generate_IDnum(l) # genererar ett unikt ID för kund
        Bank.kundinfo.append([ID, name, pnr])
        Account.add_account(pnr) # skapar ett första konto för nya kunden, känns givet hos en bank
        print(name, "är nu tillagd som kund hos NBI Bank")
        return Bank.kundinfo, True

    def generate_IDnum(num):      
        while num in Bank.kundinfo:
            num += 1
        num = f"{num:05}"
        return num
    
    def change_customer_name(new_name, pnr):
        
        for e in Bank.kundinfo:
            if e[2] == pnr:# kollar så pnr redan finns i kundlistan
                e[1] = new_name 
                return Bank.kundinfo
        return
    
    def remove_customer(pnr):
        for e in Bank.kundinfo:
            if e[2] == pnr:# kollar så pnr redan finns i kundlistan
                Bank.kundinfo = Bank.kundinfo[:e-1] + Bank.kundinfo[e+1:]
        return 
    pass

# ID, namn, personnummer, konton, transaktioner
# lista med element som detta [ID, namn, pnr, konton]

class Account():
    def add_account(pnr):
        ind = [rows[2] == pnr for rows in Bank.kundinfo].index(True)
        newaccnum = Account.generate_acc() # genererar nytt ID för konto
        Bank.kundinfo[ind].append(newaccnum) # lägger till i min Bank.kundinfo
        Bank.kundinfo[ind].append('debit account')
        saldo = 0 
        Bank.kundinfo[ind].append(saldo)
        
        return Bank.kundinfo

    
    def generate_acc():
        acc = 1001
        restart = True
        while restart:
            restart = False
            rows = len(Bank.kundinfo)
            for r in range(rows):
                c = len(Bank.kundinfo[r])
                for c in range(c):
                    if str(acc) == Bank.kundinfo[r][c]:
                        acc += 1
                        restart = True

        return str(acc)
               
    def get_account(pnr, account_id):
        rows = len(Bank.kundinfo) #loopa igenom listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): # kolla så att konto och pnr stämmer
                    saldo = Bank.kundinfo[r][c+2] 
                    return print("Du har",saldo,"kr på konto:",account_id,"(debit account)")
        return print("Konto och personnummer matchar inte.") # fångar alla misstag

    def deposit(pnr, account_id, amount):
        rows = len(Bank.kundinfo) #loopa igenom hela listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): 
                    #kolla så att konto och pnr stämmer överens
                    saldo = int(Bank.kundinfo[r][c+2]) + amount
                    Bank.kundinfo[r][c+2] = str(saldo) #skriver in i Bank.kundinfo
                    return print("Du har nu",saldo,"kr på kontot med nummer:",account_id, "\nDin insättning var", amount, "kr")
        
        return print("Något blev fel. Kontrollera uppgifter.") #fångar de fall när det inte stämmer


    def withdraw(pnr, account_id, amount):
        rows = len(Bank.kundinfo) #loopa igenom hela listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): 
                    #kolla så att konto och pnr stämmer överens
                    saldo = int(Bank.kundinfo[r][c+2])
                    if amount < saldo:
                        saldo -= amount
                        Bank.kundinfo[r][c+2] = str(saldo) #skriver in i Bank.kundinfo
                    return print("Du har nu - ",saldo,"kr - på konto med nummer:",account_id, "\nDitt uttag var", amount, "kr")
        
        return print("Något blev fel. Kontrollera uppgifter.") #fångar de fall när det inte stämmer
        

    def close_account(pnr, account_id):
        rows = len(Bank.kundinfo) #loopa igenom hela listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): 
                    #kolla så att konto och pnr stämmer överens
                    remov_saldo = Bank.kundinfo[r][c+2]
                    remov_acc = Bank.kundinfo[r][0:c] + Bank.kundinfo[r][c+3:]
                    #remov_acc.append(account_id)
                    #remov_acc.append('terminated')
                    Bank.kundinfo[r] = remov_acc
                    
                    return print("Konto med nummer:", account_id, ", tas bort. Det fanns", remov_saldo, "kr på kontot.")
                    
        return -1
    pass

#saldo, kontotyp (debit Account) och kontonummer

'''
class menu():
    def mainmenu():
        cont = 1
        val = input("Välkommen till NBI Bank!\n Vänligen välj vad du vill göra enligt nedan:\n 1. Ladda kundlista\n 2. Lägg till ny kund\n 3. Ta bort kund\n 4. Kolla saldo för kund\n")
        while cont == 1:
            name = input("Vänligen ange namn:\n")
            pnr = input("Ange personnummer (i format yyyymmdd):\n")
            nykund = Customer.add_customer(name, pnr)
            if nykund:
                print("\nKund tillagd OK.\n")
            else:
                print("Kund finns redan.")
            nyttkonto = input("Vill du även skapa ett konto för denna person? y/n \n")
            if nyttkonto == 'y':
                #Customer.add_account(pnr)
            else:
                return None
            
            
        return 

    def cust_menu(pnr):
        
        return

    def acc_menu(pnr):
        return

    pass
'''
#{def _load():●Läser in text filen och befolkar listan som ska innehålla kunderna.
#def get_customers():●Returnerar bankens alla Bank.kundinfo (personnummer och namn) 
#def add_customer(name, pnr):●Skapar en ny kund med namn och personnummer. Kunden skapas endast om det inte finns någon kund med personnumret som angetts. Returnerar True om kunden skapades annars returneras False.
#def get_customer(pnr):●Returnerar information om kunden inklusive dennes konton. Första platsen i listan är förslagsvis reserverad för kundens namn och personnummer sedan följer informationen om kundens konton.
#def change_customer_name(name, pnr)●Byter namn på kund, returnerar True om namnet ändrades annars returnerar det False(om kunden inte fanns).
#def remove_customer(pnr)●Tar bort kund med personnumret som angetts ur banken, alla kundens eventuella konton tas också bort och resultatet returneras. Listan som returneras ska innehålla information om alla konton som togs bort, saldot som kunden får tillbaka.
#def add_account(pnr)●Skapar ett konto till kunden med personnumret som angetts, returnerar kontonumret som det skapade kontot fick alternativt returneras –1 om inget konto skapades.
#def get_account(pnr, account_id)●Returnerar Textuell presentation av kontot med kontonummer som tillhör kunden (kontonummer, saldo, kontotyp).
#def deposit(pnr, account_id, amount)●Gör en insättning på kontot, returnerar True om det gick bra annars False.
#def withdraw(pnr, account_id, amount)●Gör ett uttag på kontot, returnerar True om det gick bra annars False.
#def close_account(pnr, account_id)●Avslutar ett konto. Textuell presentation av kontots saldo ska genereras och returneras.
#(VG) def get_all_transactions_by_pnr_acc_nr( pnr, acc_nr ):●Returnerar alla transaktioner som en kund har gjort med ett specifikt konto eller -1 om kontot inte existerar.}