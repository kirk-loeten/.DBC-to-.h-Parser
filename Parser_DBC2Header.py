from datetime import datetime

## Hier den Dateinamen eintragen
filename = "CSS-Electronics-OBD2-v1.3" 

g = open(filename + ".h", "w", encoding="utf-8")
g.write("/*******************************************************/\n")
g.write("// Automatisch generierter Header aus CANoe DBC-File\n") 
g.write("// Quell-Dateiname: {0}.dbc\n".format(filename)) 
g.write("// Erstelldatum: {0}\n".format(datetime.now().strftime("%Y-%m-%d"))) 
g.write("/*******************************************************/\n")
                
with open(filename + ".dbc", "r", encoding="iso-8859-1") as openfileobject:
    for line in openfileobject:
        #lineSeg = line.split(' ')
        if len(line) > 3:
            BO = ""
            if line.startswith('BO_'):
                bo = line.split(":")
                bo[0] = bo[0].strip().split(" ")
                bo[1] = bo[1].strip().split(" ")
                #Botschaft
                g.write("\n")
                g.write("/*******************************************************/\n")
                g.write("/*  Botschaft: {0}       */\n".format(bo[0][2])) 
                g.write("/*******************************************************/\n")
                g.write("#define {0}{1}_ID {2}\n".format(bo[0][0], bo[0][2], hex(int(bo[0][1]))))
                g.write("#define {0}{1}_len {2}\n".format(bo[0][0], bo[0][2], bo[1][0]))
                BO = bo[0][2]
            elif line.lstrip().startswith('SG_ '):
                sg = line.split(':')
                name = ""
                #Signal
                sg[0] = sg[0].strip() # TRIM
                sg[0] = sg[0].split(" ") # trenne bei " "
                if len(sg[0]) == 2:
                    name = sg[0][1]
                if len(sg[0]) == 3:
                    name = sg[0][1] + "_" + sg[0][2]
                g.write("//{0} - {1}\n".format(BO, name))    
                sg[1] = sg[1].strip() # TRIM
                sg[1] = sg[1].split(" ") # trenne bei " "
                g.write("#define {0}{1}_startBit {2}\n".format(BO, name, sg[1][0].split('|')[0]))
                g.write("#define {0}{1}_countBit {2}\n".format(BO, name, sg[1][0].split('|')[1].split('@')[0]))
                g.write("#define {0}{1}_faktor {2}\n".format(BO, name, sg[1][1].split(',')[0].replace("(","")))
                g.write("#define {0}{1}_offset {2}\n".format(BO, name, sg[1][1].split(',')[1].replace(")","")))
                g.write("#define {0}{1}_min {2}\n".format(BO, name, sg[1][2].split('|')[0].replace("[","")))
                g.write("#define {0}{1}_max {2}\n".format(BO, name, sg[1][2].split('|')[1].replace("]","")))
                g.write("#define {0}{1}_unit {2}\n".format(BO, name, sg[1][3]))
            elif line.startswith('VAL_'):
                #Werte
                val = line.strip().split("\"")
                val[0] = val[0].strip().split(" ")
                print(val)
                g.write("\n")
                g.write("/*******************************************************/\n")
                g.write("/*  Signalwert: {0}       */\n".format(val[0][2])) 
                g.write("/*******************************************************/\n")
                for i in range(1, len(val)-1, 2):
                    strName = val[i].strip().replace(" ","_")
                    if i > 1:
                        strNum =  val[i-1]
                    else:
                        strNum =  val[i-1][3]
                    g.write("#define {0}{1}_{2} {3}\n".format(val[0][0], val[0][2], strName, strNum))
            else:
                pass
print("Datei angelegt")
g.close()
