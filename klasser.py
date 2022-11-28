from datetime import datetime
import math
from random import randint

class Bank():
    kundinfo = []
    def startbank(): # BANKAPP - here the magic starts
        Bank._load() # laddar in filen till lista
        Menu.mainmenu() # startar upp terminal-interface
        return 
    
    def _load(): #Läser in textfilen och befolkar listan som ska innehålla kunderna.
        load_ok = False
        with open("plugg-main\mockdata.txt", "r") as file: # fil som ska läsas in. kan behöva ta bort plugg-main och bara köra mockdata.
            data = [line.strip() for line in file]
            for line in data:
                line = line.replace("#", ":")
                Bank.kundinfo.append(line.split(":"))
                load_ok = True  
        return load_ok
    
    def _save(): # sparar ner listan till textfil
        save_ok = False
        test_lines = [':'.join(line) for line in Bank.kundinfo]
        test = '\n'.join(test_lines)
        with open("plugg-main\mockdata.txt", "w") as file: # ändra till fil som ska modifieras. satt till samma som inläsningsfil som standard
            file.write(test)
            save_ok = True
        return save_ok

    def get_customers(): #Returnerar bankens alla kunder - personnummer och namn
        kundlista = [] 
        for e in Bank.kundinfo:
            kundlista.append(e[2:0:-1])
        return print(*kundlista, sep="\n")
    
    pass

class Customer():
    #Bank.kundinfo = [] # BIG LIST INFO - här är allt. Vet inget bättre sätt
    def add_customer(name, pnr): # lägger till ny kund i listan 
        datum = datetime.now().strftime("%Y%m%d") 
        if int(datum) - int(pnr) < 180000: #differens mellan dagens datum och födelsedatum. <180000 blir minderårig
            return print("Kund under 18."), False
        l = len(Bank.kundinfo) + 1
    
        if any([e[2] == pnr for e in Bank.kundinfo]): # kollar så inte pnr redan finns i kundlistan
            return print("Kund med personnummer: ",pnr," finns redan."), False
        
        ID = Customer.generate_IDnum(l) # genererar ett unikt ID för kund
        Bank.kundinfo.append([ID, name, pnr])
        print(name, "är nu tillagd som kund hos NBI Bank")
        Account.add_account(pnr) # skapar ett första konto för nya kunden, känns givet hos en bank
        return Bank.kundinfo, True

    def generate_IDnum(num): # genererar unikt ID för varje ny kund, anropas endast av add_customer 
        while num in Bank.kundinfo:
            num += 1
        num = f"{num:05}"
        return num
    
    def change_customer_name(pnr, new_name): # byter namn på önskad kund
        
        for e in Bank.kundinfo:
            if e[2] == pnr:# kollar så pnr redan finns i kundlistan
                old_name = e[1]
                e[1] = new_name 
                return print("Namnbyte OK.", old_name, "är nu registrerad som", new_name)
        
        return print("\nNågot blev fel. Kontrollera uppgifter och försök igen.")
    
    def remove_customer(pnr): # plockar bort kunden med alla dess konton, returnerar stängda konton och totala summan kunden hade 
        test = []
        all_good = False
        for e in Bank.kundinfo:
            if e[2] == pnr: #lägger alla rader som inte innehåller önskat pnr i en ny lista. 
                all_good = True
                name = e[1]
                removed_accs = e[3:-1:3]    # sparar undan konton som stängs
                saldon = list(map(float,e[5::3]))
                totsaldo = math.fsum(saldon) # sparar totala saldot 
            else:
                test.append(e)
        if all_good:
            Bank.kundinfo = test    # skriver över ny lista som standard. 
            return print(name, "är borttagen från NBI Bank.\nKonton som togs bort:", removed_accs, "med ett totalt saldo av: ", totsaldo)
        else: 
            return print("\nNågot blev fel. Kontrollera uppgifter och försök igen.")
    
    def get_customer(pnr): # printar all info som finns i listan för personen
        for e in Bank.kundinfo:
            if e[2] == pnr:
                cust = e[1:]
                return print(cust)
        return print("\nNågot blev fel. Kontrollera uppgifter och försök igen.")    
    
    pass

class Account(): 
    def add_account(pnr): # öppnar nytt konto till aktuell kund
        for rows in Bank.kundinfo:
            if rows[2] == pnr:
                newaccnum = Account.generate_acc() # genererar nytt ID för konto
                rows.append(newaccnum) # lägger till i min Bank.kundinfo
                rows.append('debit account') # typ av konto
                rows.append('0') # startsaldo av 0 kr
                print("Nytt konto öppnat för", pnr,"! Kontonummer:", newaccnum)
                return
        
        print("\nNågot blev fel. Kontrollera uppgifter och försök igen.")
        return
    
    def generate_acc(): # genererar nytt kontonummer, anropas endast av add_account
        acc = randint(1,99999) 
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
        acc = f"{acc:05}"
        return str(acc)
               
    def get_account(pnr, account_id): # spottar ut saldo och kontotyp 
        rows = len(Bank.kundinfo) #loopa igenom listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): # kolla så att konto och pnr stämmer
                    saldo = Bank.kundinfo[r][c+2] 
                    return print("Du har",saldo,"kr på konto:",account_id,"(debit account)")
        return print("\nNågot blev fel. Kontrollera uppgifter och försök igen.") # fångar alla misstag

    def deposit(pnr, account_id, amount): # sätt in pengar
        if float(amount) <= 0:
            return print("Insättning inte OK.")
        rows = len(Bank.kundinfo) #loopa igenom hela listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): #kolla så att konto och pnr stämmer överens
                    saldo = float(Bank.kundinfo[r][c+2]) + float(amount)
                    Bank.kundinfo[r][c+2] = str(saldo) #skriver in i Bank.kundinfo
                    return print("Du har nu",saldo,"kr på kontot med nummer:",account_id, "\nDin insättning var", amount, "kr")
        
        return print("Något blev fel. Kontrollera uppgifter och försök igen.") #fångar de fall när det inte stämmer

    def withdraw(pnr, account_id, amount): # ta ut pengar om det finns tillräckligt på kontot
        if float(amount) <= 0:
            return print("Uttagssumma inte OK.")
        rows = len(Bank.kundinfo) #loopa igenom hela listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): 
                    #kolla så att konto och pnr stämmer överens
                    saldo = float(Bank.kundinfo[r][c+2])
                    amount = float(amount)
                    if amount <= saldo:
                        saldo -= amount
                        Bank.kundinfo[r][c+2] = str(saldo) #skriver in i Bank.kundinfo
                    elif amount > saldo:
                        return(print("Saldo inte tillräckligt."))
                    return print("Du har nu - ",saldo,"kr - på konto med nummer:",account_id, "\nDitt uttag var", amount, "kr")
        
        return print("\nNågot blev fel. Kontrollera uppgifter och försök igen.") #fångar de fall när det inte stämmer
        
    def close_account(pnr, account_id): # stäng konto och ge feedback på hur mycket som fanns på kontot
        rows = len(Bank.kundinfo) #loopa igenom hela listan
        for r in range(rows):
            columns = len(Bank.kundinfo[r])
            for c in range(columns):
                if (account_id == Bank.kundinfo[r][c]) and (pnr == Bank.kundinfo[r][2]): 
                    #kolla så att konto och pnr stämmer överens
                    remov_saldo = Bank.kundinfo[r][c+2]
                    remov_acc = Bank.kundinfo[r][0:c] + Bank.kundinfo[r][c+3:] # slicea bort kontot som stängdes
                    Bank.kundinfo[r] = remov_acc
                    
                    return print("Konto med nummer:", account_id, ", tas bort. Det fanns", remov_saldo, "kr på kontot.")
                    
        return print("\nNågot blev fel. Kontrollera uppgifter och försök igen.")
    
    pass

class Menu():
    def mainmenu():
        running = 1
        startuptext = (
            '\n[[--Välkommen till NBI Bank--]]  ' 
        )
        print(startuptext)
        menutext = ( '\nVänligen välj vad du vill göra enligt nedan: \n(Skriv numret och sen Enter)'
            '\n 1. Skriv ut kundlista \n 2. Lägg till ny kund \n 3. Ta bort kund \n 4. Ändra namn på kund '
            '\n 5. Visa specifik kunds information \n 6. Visa specifikt konto \n 7. Öppna nytt konto för befintlig kund ' 
            '\n 8. Sätt in pengar \n 9. Ta ut pengar \n 10. Stäng konto \n 11. Visa all data i banken '
            '\n 12. Spara och stäng app\n 13. Stäng utan att spara\n'
        )
        while running:
            val = input(menutext)
            if val == '1': # get_customers
                print('\n Personnummer och namn på NBI-kunder\n')
                Bank.get_customers()
                print('\n')
                continue
            elif val == '2':  # add_customer   
                print("\n---Ny kund---")
                name = input("\nAnge namn på ny kund: ")
                pnr = input("Ange personnummer (yyyymmdd): ")
                Customer.add_customer(name, pnr)             
                continue
            elif val == '3':  # remove_customer
                print("\n---Ta bort kund---")
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")
                Customer.remove_customer(pnr)
                continue
            elif val == '4':  # change_customer_name    
                print("\n---Ändra namn på kund---")
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")
                new_name = input("Ange önskat nytt namn: ")  
                Customer.change_customer_name(pnr, new_name)      
                continue
            elif val == '5':  # get_customer   
                print("\n---Visa kundinfo och konton---") 
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")
                Customer.get_customer(pnr)    
                continue
            elif val == '6':  # get_account    
                print("\n---Visa konto---") 
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")
                account_id = input("Ange kontonummer: ") 
                Account.get_account(pnr, account_id)        
                continue
            elif val == '7':  # add_account
                print("\n---Öppna nytt konto---")      
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")       
                Account.add_account(pnr) 
                continue
            elif val == '8':  # deposit    
                print("\n---Sätta in pengar---")     
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")     
                account_id = input("Vilket konto vill du sätta in pengar på? ")
                amount = input("Hur mycket vill du sätta in? ")
                Account.deposit(pnr, account_id, amount)
                continue
            elif val == '9':  # withdraw   
                print("\n---Ta ut pengar---")
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")     
                account_id = input("Vilket konto vill du ta ut pengar från? ")
                amount = input("Hur mycket vill du ta ut? ")
                Account.withdraw(pnr, account_id, amount)            
                continue
            elif val == '10': # close_account   
                print("\n---Stänga konto---")
                pnr = input("\nAnge kundens personnummer (yyyymmdd): ")     
                account_id = input("Ange kontonummer som önskas termineras: ")       
                Account.close_account(pnr, account_id)    
                continue
            elif val == '11': # printa hela listan kundinfo
                print("\n---All NBIBank kundinfo---\n")
                print(*Bank.kundinfo, sep="\n")       
                print('\n')    
                continue
            elif val == '12': # _save      
                Bank._save()
                print("\n\nSparat och klart. Avslutar...\nPå återseende!\n\n")
                running = 0         
                break
            elif val == '13': # bara avsluta loop
                print('\n\nAvslutat! På återseende!\n')
                running = 0         
                break
            else:
                print("\nFel input, försök igen. ")
            
            
        return 

    pass

