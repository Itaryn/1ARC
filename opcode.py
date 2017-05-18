import chip8, lecture
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
    if chip8.memoire[chip8.PC+1] < 0x10:
        val = '0' + str(hex(chip8.memoire[chip8.PC+1])[2:])
    else:
        val = str(hex(chip8.memoire[chip8.PC+1])[2:])
    # opcode correspond à la valeur hexadécimale de 4 octets
    opcode = int(str(hex(chip8.memoire[chip8.PC])) + val, 16)
    # On va tester chaque opcodeId pour trouver celui qui correspond à notre valeur
    for i in range(34):
        if opcode & opcodeMasque[i] == opcodeId[i]:
            # On retourne l'id qui correspond à notre opcodeId
            return i, opcode
    # Si on ne trouve pas de valeur on renvoit 0 (une erreur)
    return 0, 0

# Va faire la fonction adapté à l'id trouvé

def interpretation():
    # On utilise la fonction analyse pour récupérer notre action et notre code hexadécimale
    action, opcode = analyse()
    print(action, hex(opcode))
    # Si on a obtenu 0, c'est une erreur
    if action == 0:
        print("!!! Erreur !!! Aucune action à effectuer")
    elif action == 2:
        # 00EE : On revient d'un saut
        if chip8.nbrSaut > 0:
            chip8.nbrSaut -= 1
            chip8.PC = chip8.saut[chip8.nbrSaut]
    elif action == 3:
        # 1NNN : PC prend la valeur de NNN
        chip8.PC = valueNNN(opcode)
        chip8.PC -= 2
    elif action == 4:
        # 2NNN : On fait un saut
        chip8.saut[chip8.nbrSaut] = chip8.PC
        if chip8.nbrSaut < 15:
            chip8.nbrSaut += 1
        chip8.PC = valueNNN(opcode)
        chip8.PC -= 2
    elif action == 5:
        # 3XNN : On passe la prochaine instruction si la valeur de VX est égale à NN
        if chip8.V[valueX(opcode)] == valueNN(opcode):
            chip8.PC += 2
    elif action == 6:
        # 4XNN : On passe la prochaine instruction si la valeur de VX n'est pas égale à NN
        if chip8.V[valueX(opcode)] != valueNN(opcode):
            chip8.PC += 2
    elif action == 7:
        # 5XY0 : On passe la prochaine instruction si la valeur de VX est égale à la valeur de VY
        if chip8.V[valueX(opcode)] == chip8.V[valueY(opcode)]:
            chip8.PC += 2
    elif action == 8:
        # 6XNN : VX prend la valeur de NN
        chip8.V[valueX(opcode)] = valueNN(opcode)
    elif action == 9:
        # 7XNN : On ajoute NN à VX (stocké dans VX)
        chip8.V[valueX(opcode)] += valueNN(opcode)
        if chip8.V[valueX(opcode)] > 255:
            chip8.V[valueX(opcode)] = 255
    elif action == 10:
        # 8XY0 : VX prend la valeur de VY
        chip8.V[valueX(opcode)] = chip8.V[valueY(opcode)]
    elif action == 11:
        # 8XY1 : VX prend la valeur de VX OU LOGIQUE VY
        chip8.V[valueX(opcode)] = (chip8.V[valueX(opcode)] | chip8.V[valueY(opcode)])
    elif action == 12:
        # 8XY2 : VX prend la valeur VX ET LOGIQUE VY
        chip8.V[valueX(opcode)] = (chip8.V[valueX(opcode)] & chip8.V[valueY(opcode)])
    elif action == 13:
        # 8XY3 : VX prend la valeur VX XOR LOGIQUE VY
        chip8.V[valueX(opcode)] = (chip8.V[valueX(opcode)] ^ chip8.V[valueY(opcode)])
    elif action == 14:
        # 8XY4 : On ajoute VY à VX (stocké dans VX) si on dépasse 255, on met VF à 1 (carry)
        if (chip8.V[valueX(opcode)] + chip8.V[valueY(opcode)]) > 255:
            chip8.V[0xF] = 1
        else:
            chip8.V[0xF] = 0
        chip8.V[valueX(opcode)] += (valueY(opcode) - chip8.V[0xF])
    elif action == 15:
        # 8XY5 : On retire VY à VX (stocké dans VX) si VX > VY, on met VF à 1
        if chip8.V[valueX(opcode)] > chip8.V[valueY(opcode)]:
            chip8.V[0xF] = 1
        else:
            chip8.V[0xF] = 0
        chip8.V[valueX(opcode)] -= chip8.V[valueY(opcode)]
    elif action == 16:
        # 8XY6 : On déplace tous les bits de VX de 1 vers la droite (ou division par 2)
        # Si VX était impair on met VF à 1
        if chip8.V[valueX(opcode)] % 2 == 1:
            chip8.V[0xF] = 1
        else:
            chip8.V[0xF] = 0
        chip8.V[valueX(opcode)] = (chip8.V[valueX(opcode)] - chip8.V[0xF]) / 2
    elif action == 17:
        # 8XY7 : On retire VX à VY (stocké dans VX) si VY > VX, on met VF à 1
        if chip8.V[valueY(opcode)] > chip8.V(valueX(opcode)):
            chip8.V[0xF] = 1
        else:
            chip8.V[0xF] = 0
        chip8.V[valueX(opcode)] = chip8.V[valueY(opcode)] - chip8.V[valueX(opcode)]
    elif action == 18:
        # 8XYE : On déplace tous les bits de VX de 1 vers la gauche (ou multiplication par 2)
        # Si VX était supérieur à 128 on met VF à 1
        if chip8.V[valueX(opcode)] >= 128:
            chip8.V[0xF] = 1
        else:
            chip8.V[0xF] = 0
        chip8.V[valueX(opcode)] = (chip8.V[valueX(opcode)] - chip8.V[0xF]*128) * 2
    elif action == 19:
        # 9XY0 : On passe la prochaine instruction si la valeur de VX n'est pas égale à la valeur de VY
        if chip8.V[valueX(opcode)] != chip8.V[valueY(opcode)]:
            chip8.PC += 2
    elif action == 20:
        # ANNN : I prend la valeur NNN
        chip8.I = valueNNN(opcode)
    elif action == 21:
        # BNNN : PC augmente de la valeur NNN
        chip8.PC = chip8.V[0] + valueNNN(opcode)
        chip8.PC -= 2
    elif action == 22:
        # CXNN : VX prend une valeur random entre 0 et 255 avec un ET LOGIQUE avec NN
        chip8.V[valueX(opcode)] = random.randint(0, 255) & valueNN(opcode)
    elif action == 24:
        # EX9E : On saute la prochaine instruction si la touche qui a la valeur de VX est pressée
        if chip8.tabTouche[chip8.V[valueX(opcode)]] == 1:
            chip8.PC += 2
    elif action == 25:
        # EXA1 : On saute la prochaine instruction si la touche qui a la valeur de VX n'est pas pressée
        if chip8.tabTouche[chip8.V[valueX(opcode)]] == 0:
            chip8.PC += 2
    elif action == 26:
        # FX07 : VX prend la valeur de DT
        chip8.V[valueX(opcode)] = chip8.DT
    elif action == 28:
        # FX15 : DT prend la valeur de VX
        chip8.DT = chip8.V[valueX(opcode)]
    elif action == 29:
        # FX18 : ST prend la valeur de VX
        chip8.ST = chip8.V[valueX(opcode)]
    elif action == 30:
        # FX1E : On ajoute VX à I (stockée dans I)
        if chip8.I + chip8.V[valueX(opcode)] > 0xFFF:
            chip8.V[0xF] = 1
        else:
            chip8.V[0xF] = 0
        chip8.I += chip8.V[valueX(opcode)] - chip8.V[0xF]
    elif action == 31:
        # FX29 : I prend la valeur de VX
        chip8.I = 5 * chip8.V[valueX(opcode)]
    elif action == 32:
        # FX33
        print()
    elif action == 33:
        # FX55
        for i in range(valueX(opcode)):
            chip8.memoire[chip8.I+i] = chip8.V[i]
    elif action == 34:
        # FX65
        for i in range(valueX(opcode)):
            chip8.V[i] = chip8.memoire[chip8.I+i]
    else:
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