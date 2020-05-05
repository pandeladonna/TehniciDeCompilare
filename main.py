from analizor import Analizor

PATH_TO_ATOM_TABLE = r"E:\dragulici tema 1\LabLFTCAnalizor\atomtable.txt"
PATH_TO_FILE = r"E:\dragulici tema 1\LabLFTCAnalizor\p3.txt"

def parseTableFromFile(file):
    dict = {}
    with open(file,"r") as f:
        line = f.readline().strip()
        while line != "":
            elems = line.split(" ")
            if elems[0]!="ATOM":
                dict[elems[0]] = elems[1]
            line = f.readline().strip()
    return dict



predefTable = parseTableFromFile(PATH_TO_ATOM_TABLE)
analizor = Analizor(predefTable,PATH_TO_FILE)
analizor.parsare()

print("PREDEF TABLE: ")
print(analizor.getPredefTable())
print()

print("FIP")
for elem in analizor.getFip():
    print(elem)

print()
print("IDENTIFICATOR TABLE")
print(analizor.getIDTable())
print()
print("CONSTANT TABLE")
print(analizor.getConstTable())