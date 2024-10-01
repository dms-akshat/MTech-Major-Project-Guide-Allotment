delim = ","
 
with open("preference.csv", "r") as file:
    lines = [map(str.strip, line.split(delim)) for line in file]
 
with open("preference.csv", "w") as file:
    for line in lines:
        file.write(",".join(line)+"\n")