import chip8
fichierSauve = open('test.txt', 'w')
for x in chip8.memoire:
    fichierSauve.write(str(x)+'\n')
for x in chip8.V:
    fichierSauve.write(str(x)+'\n')
fichierSauve.write(str(chip8.I)+'\n')
fichierSauve.write(str(chip8.DT)+'\n')
fichierSauve.write(str(chip8.ST)+'\n')
fichierSauve.write(str(chip8.PC)+'\n')
fichierSauve.write(str(chip8.SP)+'\n')
for x in chip8.saut:
    fichierSauve.write(str(x)+'\n')
fichierSauve.write(str(chip8.nbrSaut)+'\n')
for x in chip8.tabEcran:
    for y in x:
        fichierSauve.write(str(y)+'\n')
fichierSauve.close()