import memoire, lecture
import random

# Ces 2 listes vont nous permettre de retrouver l'opcode de référence (opcodeId)
# de l'hexadécimale stocké en mémoire

opcodeMasque = [0x0000, 0xFFFF, 0xFFFF, 0xF000, 0xF000,
                0xF000, 0xF000, 0xF00F, 0xF000, 0xF000,
                0xF00F, 0xF00F, 0xF00F, 0xF00F, 0xF00F,
                0xF00F, 0xF00F, 0xF00F, 0xF00F, 0xF00F,
                0xF000, 0xF000, 0xF000, 0xF000, 0xF0FF,
                0xF0FF, 0xF0FF, 0xF0FF, 0xF0FF, 0xF0FF,
                0xF0FF, 0xF0FF, 0xF0FF, 0xF0FF, 0xF0FF]

opcodeId = [0x0FFF, 0x00E0, 0x00EE, 0x1000, 0x2000,
            0x3000, 0x4000, 0x5000, 0x6000, 0x7000,
            0x8000, 0x8001, 0x8002, 0x8003, 0x8004,
            0x8005, 0x8006, 0x8007, 0x800E, 0x9000,
            0xA000, 0xB000, 0xC000, 0xD000, 0xE09E,
            0xE0A1, 0xF007, 0xF00A, 0xF015, 0xF018,
            0xF01E, 0xF029, 0xF033, 0xF055, 0xF065]

# Analyse le code hexadécimal stocké en mémoire à l'adresse du PC

def analyse():
    # On va regarder si la valeur à PC+1 est inférieur à 0x10 (16 en décimal)
    # Cela nous permet d'obtenir un hexa de 4 octet à la fin
    if memoire.memoire[memoire.PC+1] < 0x10:
        val = '0' + str(hex(memoire.memoire[memoire.PC+1])[2:])
    else:
        val = str(hex(memoire.memoire[memoire.PC+1])[2:])
    # opcode correspond à la valeur hexadécimale de 4 octets
    opcode = int(str(hex(memoire.memoire[memoire.PC])) + val, 16)
    # On va tester chaque opcodeId pour trouver celui qui correspond à notre valeur
    for i in range(35):
        if opcode & opcodeMasque[i] == opcodeId[i]:
            # On retourne l'id qui correspond à notre opcodeId
            return i, opcode
    # Si on ne trouve pas de valeur on renvoit 0 (une erreur)
    return 0, 0

# Va faire la fonction adapté à l'id trouvé

def interpretation():
    # On utilise la fonction analyse pour récupérer notre action et notre code hexadécimale
    action, opcode = analyse()
    if action == 2:
        # 00EE : On revient d'un saut
        if memoire.SP > 0:
            memoire.SP -= 1
            memoire.PC = memoire.saut[memoire.SP]
    elif action == 3:
        # 1NNN : PC prend la valeur de NNN
        memoire.PC = valueNNN(opcode)
        memoire.PC -= 2
    elif action == 4:
        # 2NNN : On fait un saut
        memoire.saut[memoire.SP] = memoire.PC
        if memoire.SP < 15:
            memoire.SP += 1
        memoire.PC = valueNNN(opcode)
        memoire.PC -= 2
    elif action == 5:
        # 3XNN : On passe la prochaine instruction si la valeur de VX est égale à NN
        if memoire.V[valueX(opcode)] == valueNN(opcode):
            memoire.PC += 2
    elif action == 6:
        # 4XNN : On passe la prochaine instruction si la valeur de VX n'est pas égale à NN
        if memoire.V[valueX(opcode)] != valueNN(opcode):
            memoire.PC += 2
    elif action == 7:
        # 5XY0 : On passe la prochaine instruction si la valeur de VX est égale à la valeur de VY
        if memoire.V[valueX(opcode)] == memoire.V[valueY(opcode)]:
            memoire.PC += 2
    elif action == 8:
        # 6XNN : VX prend la valeur de NN
        memoire.V[valueX(opcode)] = valueNN(opcode)
    elif action == 9:
        # 7XNN : On ajoute NN à VX (stocké dans VX)")
        memoire.V[valueX(opcode)] += valueNN(opcode)
        if memoire.V[valueX(opcode)] > 0b11111111:
            memoire.V[valueX(opcode)] -= 0b100000000
    elif action == 10:
        # 8XY0 : VX prend la valeur de VY
        memoire.V[valueX(opcode)] = memoire.V[valueY(opcode)]
    elif action == 11:
        # 8XY1 : VX prend la valeur de VX OU LOGIQUE VY
        memoire.V[valueX(opcode)] = (memoire.V[valueX(opcode)] | memoire.V[valueY(opcode)])
    elif action == 12:
        # 8XY2 : VX prend la valeur VX ET LOGIQUE VY
        memoire.V[valueX(opcode)] = (memoire.V[valueX(opcode)] & memoire.V[valueY(opcode)])
    elif action == 13:
        # 8XY3 : VX prend la valeur VX XOR LOGIQUE VY
        memoire.V[valueX(opcode)] = (memoire.V[valueX(opcode)] ^ memoire.V[valueY(opcode)])
    elif action == 14:
        # 8XY4 : On ajoute VY à VX (stocké dans VX) si on dépasse 255, on met VF à 1 (carry)
        memoire.V[valueX(opcode)] += memoire.V[valueY(opcode)]
        if memoire.V[valueX(opcode)] > 0b11111111:
            memoire.V[0xF] = 1
            memoire.V[valueX(opcode)] -= 0b100000000
        else:
            memoire.V[0xF] = 0
    elif action == 15:
        # 8XY5 : On retire VY à VX (stocké dans VX) si VX > VY, on met VF à 1
        if memoire.V[valueX(opcode)] > memoire.V[valueY(opcode)]:
            memoire.V[0xF] = 1
        else:
            memoire.V[0xF] = 0
        memoire.V[valueX(opcode)] -= memoire.V[valueY(opcode)]
        if memoire.V[valueX(opcode)] < 0:
            memoire.V[valueX(opcode)] += 0b100000000
    elif action == 16:
        # 8XY6 : On déplace tous les bits de VX de 1 vers la droite (ou division par 2)
        # Si VX était impair on met VF à 1
        if memoire.V[valueX(opcode)] % 2 == 1:
            memoire.V[0xF] = 1
        else:
            memoire.V[0xF] = 0
        memoire.V[valueX(opcode)] = int((memoire.V[valueX(opcode)] - memoire.V[0xF]) / 2)
    elif action == 17:
        # 8XY7 : On retire VX à VY (stocké dans VX) si VY > VX, on met VF à 1
        if memoire.V[valueY(opcode)] > memoire.V[valueX(opcode)]:
            memoire.V[0xF] = 1
        else:
            memoire.V[0xF] = 0
        memoire.V[valueX(opcode)] = memoire.V[valueY(opcode)] - memoire.V[valueX(opcode)]
        if memoire.V[valueY(opcode)] < 0:
            memoire.V[valueX(opcode)] += 0b100000000
    elif action == 18:
        # 8XYE : On déplace tous les bits de VX de 1 vers la gauche (ou multiplication par 2)")
        # Si VX était supérieur à 128 on met VF à 1
        if memoire.V[valueX(opcode)] >= 0b10000000:
            memoire.V[0xF] = 1
        else:
            memoire.V[0xF] = 0
        memoire.V[valueX(opcode)] = int((memoire.V[valueX(opcode)] - memoire.V[0xF]*128) * 2)
    elif action == 19:
        # 9XY0 : On passe la prochaine instruction si la valeur de VX n'est pas égale à la valeur de VY
        if memoire.V[valueX(opcode)] != memoire.V[valueY(opcode)]:
            memoire.PC += 2
    elif action == 20:
        # ANNN : I prend la valeur NNN
        memoire.I = valueNNN(opcode)
    elif action == 21:
        # BNNN : PC augmente de la valeur NNN
        memoire.PC = memoire.V[0] + valueNNN(opcode)
        memoire.PC -= 2
    elif action == 22:
        # CXNN : VX prend une valeur random entre 0 et 255 avec un ET LOGIQUE avec NN
        memoire.V[valueX(opcode)] = random.randint(0, 255) & valueNN(opcode)
    elif action == 24:
        # EX9E : On saute la prochaine instruction si la touche qui a la valeur de VX est pressée
        if memoire.tabTouche[memoire.V[valueX(opcode)]] == 1:
            memoire.PC += 2
    elif action == 25:
        # EXA1 : On saute la prochaine instruction si la touche qui a la valeur de VX n'est pas pressée
        if memoire.tabTouche[memoire.V[valueX(opcode)]] == 0:
            memoire.PC += 2
    elif action == 26:
        # FX07 : VX prend la valeur de DT
        memoire.V[valueX(opcode)] = memoire.DT
    elif action == 28:
        # FX15 : DT prend la valeur de VX
        memoire.DT = memoire.V[valueX(opcode)]
    elif action == 29:
        # FX18 : ST prend la valeur de VX
        memoire.ST = memoire.V[valueX(opcode)]
    elif action == 30:
        # FX1E : On ajoute VX à I (stockée dans I) et on met VF à 1 si I est supérieur à 0xFFF
        memoire.I += memoire.V[valueX(opcode)]
        if memoire.I > 0xFFF:
            memoire.I -= 0x1000
    elif action == 31:
        # FX29 : I prend la valeur du caractère au numéro de VX
        memoire.I = 5 * memoire.V[valueX(opcode)]
    elif action == 32:
        # FX33 : On stocke en mémoire à l'adress I (centaine), I+1 (dizaine) et I+2 (unité) la valeur de VX
        memoire.memoire[memoire.I] = (memoire.V[valueX(opcode)] - memoire.V[valueX(opcode)] % 100) / 100
        memoire.memoire[memoire.I + 1] = (((memoire.V[valueX(opcode)] - memoire.V[valueX(opcode)] % 10) / 10) % 10)
        memoire.memoire[memoire.I + 2] = memoire.V[valueX(opcode)] - memoire.memoire[memoire.I] * 100 - 10 * memoire.memoire[memoire.I + 1]
    elif action == 33:
        # FX55 : On stocke les valeurs de V0 à VX en mémoire à partir de I
        for i in range(valueX(opcode) + 1):
            memoire.memoire[memoire.I+i] = memoire.V[i]
    elif action == 34:
        # FX65 : On prend les valeurs en mémoire à partir de I que l'on met dans V0 à VX
        for i in range(valueX(opcode) + 1):
            memoire.V[i] = int(memoire.memoire[memoire.I+i])
    else:
        # Si aucun opcode n'a match ce n'est pas normal
        if action != 1 and action != 23 and action != 27:
            print("!!! Erreur !!!")
    return action, opcode

# Fonction qui va renvoyer la valeur d'un NNN

def valueNNN(opcode):
    return int(hex(opcode)[3:], 16)

# Fonction qui va renvoyer la valeur d'un NN

def valueNN(opcode):
    return int(hex(opcode)[4:], 16)

# Fonction qui va renvoyer la valeur d'un N

def valueN(opcode):
    return int(hex(opcode)[5:], 16)

# Fonction qui va renvoyer la valeur d'un X

def valueX(opcode):
    return int(hex(opcode)[3:4], 16)

# Fonction qui va renvoyer la valeur d'un Y

def valueY(opcode):
    return int(hex(opcode)[4:5], 16)