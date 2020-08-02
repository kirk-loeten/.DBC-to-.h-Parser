from datetime import datetime

## Hier den Dateinamen eintragen
filename = "FILENAME" 

g = open(filename + ".h", "w", encoding="utf-8")
g.write("/*******************************************************/\n")
g.write("// Automatisch generierter Header aus CANoe DBC-File\n") 
g.write("// Quell-Dateiname: {0}.dbc\n".format(filename)) 
g.write("// Erstelldatum: {0}\n".format(datetime.now().strftime("%Y-%m-%d"))) 
g.write("/*******************************************************/\n")
                
with open(filename + ".dbc", "r", encoding="utf-8") as openfileobject:
    for line in openfileobject:
        lineSeg = line.split(' ')
        if len(lineSeg) > 3:
            if lineSeg[0] == 'BO_':
                #Botschaft
                g.write("\n")
                g.write("/*******************************************************/\n")
                g.write("/*  Botschaft: {0}       */\n".format(lineSeg[2])) 
                g.write("/*******************************************************/\n")
                g.write("#define {0}{1}_ID {2}\n".format(lineSeg[0], lineSeg[2], hex(int(lineSeg[1]))))
                g.write("#define {0}{1}_len {2}\n".format(lineSeg[0], lineSeg[2], lineSeg[4]))
                BO = lineSeg[2]
            elif lineSeg[0] == "" and lineSeg[2] == "SG_":
                #Signal
                g.write("//{0} - {1}\n".format(BO, lineSeg[3]))
                g.write("#define {0}{1}_startBit {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[5].split('|')[0]))
                g.write("#define {0}{1}_countBit {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[5].split('|')[1].split('@')[0]))
                g.write("#define {0}{1}_faktor {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[6].split(',')[0].replace("(","")))
                g.write("#define {0}{1}_offset {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[6].split(',')[1].replace(")","")))
                g.write("#define {0}{1}_min {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[7].split('|')[0].replace("[","")))
                g.write("#define {0}{1}_max {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[7].split('|')[1].replace("]","")))
                g.write("#define {0}{1}_unit {2}\n".format(lineSeg[2], lineSeg[3], lineSeg[8]))
            elif lineSeg[0] == "VAL_":
                #Werte
                g.write("\n")
                g.write("/*******************************************************/\n")
                g.write("/*  Signalwert: {0}       */\n".format(lineSeg[2])) 
                g.write("/*******************************************************/\n")
                for i in range(3, len(lineSeg)-1, 2):
                    g.write("#define {0}{1}_{2} {3}\n".format(lineSeg[0], lineSeg[2], lineSeg[i+1].replace(" ","").replace("\"",""), lineSeg[i]))
            else:
                pass
print("Datei angelegt")
g.close()
