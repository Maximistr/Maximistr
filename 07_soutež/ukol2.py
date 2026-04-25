import random

# Nastavení třídy žáka
class player_class:
    def __init__(self,name):
        self.name = name
        self.points = 0
        self.full_cat = 0
        self.numbers_cat = {"1" : [True,0],
                            "2" : [True,0],
                            "3" : [True,0],
                            "4" : [True,0],
                            "5" : [True,0],
                            "6" : [True,0]}
        self.small = [True,0, "Malé"]
        self.big = [True,0, "Velké"]
        self.even = [True,0, "Sudé"]
        self.odd = [True,0, "Liché"]
        self.duos = [True,0, "Dvoják"]
        self.trio = [True,0, "Troják"]
        self.general = [True,0, "Genrál"]
        self.straight = [True,0, "Postupka"]
        self.pyramind = [True,0, "Pyramida"]
    def basic_numbers(self,number,amount):
        self.points += number * amount
        self.numbers_cat["{0}".format(number)][0] = False
        self.numbers_cat["{0}".format(number)][1] = number * amount
        print(f"a = {amount}, n = {number}")
        self.full_cat += 1
    def availible_categories(self):
        self.categories = [self.small,self.big,self.even,self.odd, self.duos,self.trio,self.general,self.straight,self.pyramind]
        for i in range(len(self.numbers_cat)):
            print(f"{i + 1} | Kategorie : {i + 1} | Počet získaných bodů : {self.numbers_cat["{}".format(i + 1)][1]} | Dostupné? : {self.numbers_cat["{}".format(i + 1)][0]}")
        for x in range(len(self.categories)):
            print(f"{x + 7} | Kategorie : {self.categories[x][2]} | Počet získaných bodů : {self.categories[x][1]} | Dostupné? : {self.categories[x][0]}")
        print(f"Součet bodů : {self.points}")
    def add_points(self,categor,amount):
        self.categories[categor][1] = amount
        self.categories[categor][0] = False
        self.points += amount
        self.full_cat += 1

# Dostání informace o počtu a číslu hráčů
num_p = 0     
players = {}

while True:
    num_p = input("Kolik hráčů bude hrát?(2-4): ")
    try:
        num_p = int(num_p)
    except ValueError:
        print("Zadejte prosím číslo 2-4 : ")
        continue
    if num_p >= 2 and num_p <= 4:
        print(num_p)
        break
    else:
        print("Zadejte prosím číslo 2-4 :")
for player in range(num_p):
    player_name = input(f"Zadej jméno hráče číslo {player + 1}: ")
    players["p_{0}".format(player + 1)] = player_class({str(player_name)})
    
# Funkce pro spuštění tahu hráče
def turn(player):
    rethrows = 0
    dice = {}
    dice_to_reroll = []
    numbers = {"1" : 0,
                "2" : 0,
                "3" : 0,
                "4" : 0,
                "5" : 0,
                "6" : 0}
    postupka = 0
    general = [False,0]
    duos = []
    trios = []
    solo = 0
    print("Kostka | hodnota")
    for x in range(6):
        dice["die_{0}".format(x + 1)] = random.randint(1,6)
        print(f"     {x + 1} | {dice["die_{0}".format(x + 1)]}")
    while rethrows < 2:
        new_throw = input("Chcete přehodit některé kostky?(ano/ne)")
        dice_to_reroll = []
        if new_throw == "ano":
            while True:
                dice_reroll = input("Zadejte číslo jedné z kostek(pokud už nechcete hodit další kostky zadejte enter): ")
                try:
                    dice_reroll = int(dice_reroll)
                except ValueError:
                    if dice_reroll != "":
                        print("Zadejte prosím číslo platné číslo kostky")
                        continue
                    elif dice_reroll == "":
                        pass
                if dice_reroll == "":
                    rethrows += 1
                    print("Kostka | hodnota")
                    for die in range(len(dice_to_reroll)):
                        dice["die_{0}".format(dice_to_reroll[die])] = random.randint(1,6)
                    for x in range(6):
                        print(f"     {x + 1} | {dice["die_{0}".format(x + 1)]}")
                    break
                elif dice_reroll >= 1 and dice_reroll <= 6:
                    dice_to_reroll.append(dice_reroll)
                else:
                    print("Zadejte prosím číslo platné číslo kostky")
        else:
            break
    player.availible_categories()
    for value in range(6):
        numbers["{0}".format(dice["die_{0}".format(value + 1)])] += 1
    for x in range(6):
        if numbers["{0}".format(value + 1)] == 1:
            postupka += 1
            solo = x + 1
        elif numbers["{0}".format(value + 1)] == 2:
            duos.append(x + 1)
        elif numbers["{0}".format(value + 1)] == 3:
            trios.append(x + 1)
        elif numbers["{0}".format(value + 1)] == 6:
            general[0] = True
            general[1] = x + 1
    while True:
        change_cat = input("Zadejte do které kategorie chcete zapsat počet získaných bodů(číslo úplně vlevo): ")
        try:
            change_cat = int(change_cat)
        except ValueError:
            print("Zadejte prosím platné číslo kategorie.")
            continue
        if change_cat <= 6 and  change_cat >= 1:
            if player.numbers_cat["{0}".format(change_cat)][0] == True:
                player.basic_numbers(change_cat,numbers["{0}".format(change_cat)])
                break
            else:
                print("Prosím zadejte číslo dostupné kategorie.")
                continue
        
        if change_cat >= 7 and change_cat <= 16:
                if player.categories[change_cat - 7][0] == True:
                    points = 0
                    match change_cat:
                        case 7:
                            for x in range(3):
                                points += (x + 1) * numbers["{0}".format(x + 1)]
                        case 8:
                            for x in range(4,7):
                                points += (x) * numbers["{0}".format(x)]
                        case 9:
                            for x in range(6):
                                if (x + 1) % 2 == 0:
                                    points += (x + 1) * numbers["{0}".format(x + 1)]
                        case 10:
                            for x in range(6):
                                if (x + 1) % 2 != 0:
                                    points += (x + 1) * numbers["{0}".format(x + 1)]
                        case 11:
                            if len(duos) == 3:
                                for x in range(3):
                                    points += duos[x] * 2
                        case 12:
                            if len(trios) == 2:
                                for x in range(2):
                                    points += trios[x] * 3
                        case 13:
                            if general[0]:
                                points = general[1] * 6
                        case 14:
                            if postupka == 6:
                                    points = 21
                        case 15:
                            if len(trios) == 1 and len(duos) == 1:
                                if trios[0] > duos[0] > solo or trios[0] < duos[0] < solo:
                                    points = (trios[0] * 3) + (duos[0] * 2) + (solo)
                    player.add_points(change_cat - 7,points)
                    break
                else:
                    print("Prosím zadejte číslo dostupné kategorie.")
                    continue
        else:
            print("Zadejte prosím platné číslo kategorie.")
            continue
# Smyčka hry
while True:
    for play in range(len(players)):
        print(f" Tah hráče {players["p_{0}".format(play + 1)].name} ")
        turn(players["p_{0}".format(play + 1)])
        players["p_{0}".format(play + 1)].availible_categories()
    if players["p_{0}".format(len(players))].full_cat >= 15:
        break

    