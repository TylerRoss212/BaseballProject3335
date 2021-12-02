import sys
f = open("./GiveUsAnADrSpeegle.sql", "r")
#print(sys.argv[1])
members = []
for line in f:
    if line.startswith("CREATE TABLE " + sys.argv[1]):
        while not line.startswith("primary"):
            line = f.readline()

            if line != "\n":
                line = line[:-1]
                # print(line)
                # if line != ")":
                data = line.split()
                if data[0] == "primary":
                    break
                myStr = ""
                myStr += data[0]
                members.append("self." + data[0] + " = ")
                myStr += " = Column("

                typeStr = ""
                if data[1].startswith("varchar") or data[1].startswith("char"):
                    typeStr = "String("
                    numStr = ""

                    copy = False

                    for c in data[1]:
                        if c != ")" and c != "," and copy == True:
                            numStr += c

                        if c == "(":
                            copy = True

                    typeStr += numStr
                    typeStr += ")"
                elif data[1].startswith("int"):
                    typeStr = "Integer"
                elif data[1].startswith("double"):
                    typeStr = "Numeric"

                typeStr += ")"
                myStr += typeStr

                print(myStr)

        print(line)

print()

for member in members:
    print(member)

print()
f2 = open("./baseballdatabank/core/" + sys.argv[2], "r")

line = f2.readline()

i = 0
data = line.split(",")

for word in data:
    print(i, " - ", word)
    i += 1

